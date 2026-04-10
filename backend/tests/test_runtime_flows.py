import json

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.ai_providers.models import AIProvider
from apps.ai_providers.services import resolve_provider
from apps.institutes.models import Institute, InstituteMembership, Subject
from apps.library.models import Book, BookChunk


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username='user@example.com',
        email='user@example.com',
        password='StrongPass123',
        full_name='Test User',
    )


@pytest.fixture
def other_user():
    return User.objects.create_user(
        username='other@example.com',
        email='other@example.com',
        password='StrongPass123',
        full_name='Other User',
    )


@pytest.fixture
def authenticated_client(api_client, user):
    response = api_client.post(
        '/api/v1/auth/login/',
        {'email': user.email, 'password': 'StrongPass123'},
        format='json',
    )
    token = response.data['tokens']['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.fixture
def institute(user):
    return Institute.objects.create(name='Darul Ilm', slug='darul-ilm', admin=user)


@pytest.mark.django_db
def test_registration_login_and_me_endpoint(api_client):
    register_response = api_client.post(
        '/api/v1/auth/register/',
        {
            'email': 'new@example.com',
            'full_name': 'New User',
            'arabic_name': 'مستخدم جديد',
            'phone': '1234567',
            'preferred_lang_pair': 'ar-en',
            'password': 'StrongPass123',
            'password_confirm': 'StrongPass123',
        },
        format='json',
    )
    assert register_response.status_code == 201
    assert register_response.data['user']['email'] == 'new@example.com'

    login_response = api_client.post(
        '/api/v1/auth/login/',
        {'email': 'new@example.com', 'password': 'StrongPass123'},
        format='json',
    )
    assert login_response.status_code == 200

    token = login_response.data['tokens']['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    me_response = api_client.get('/api/v1/accounts/me/')
    assert me_response.status_code == 200
    assert me_response.data['email'] == 'new@example.com'


@pytest.mark.django_db
def test_institute_membership_is_scoped_to_user(authenticated_client, user, other_user, institute):
    InstituteMembership.objects.create(user=user, institute=institute, role='student', is_active=True)
    InstituteMembership.objects.create(user=other_user, institute=institute, role='student', is_active=True)

    response = authenticated_client.get('/api/v1/institutes/memberships/')
    assert response.status_code == 200
    payload = response.data['results'] if isinstance(response.data, dict) else response.data
    assert len(payload) == 1
    assert payload[0]['user_email'] == user.email


@pytest.mark.django_db
def test_book_creation_and_visibility(authenticated_client, user, other_user, institute):
    subject = Subject.objects.create(name='Nahw', slug='nahw')
    upload = SimpleUploadedFile('lesson.txt', b'Arabic text content', content_type='text/plain')

    create_response = authenticated_client.post(
        '/api/v1/library/books/',
        {
            'title': 'Al Ajrumiyyah',
            'author': 'Ibn Ajurrum',
            'language': 'Arabic',
            'visibility': 'private',
            'subject': subject.id,
            'file': upload,
            'file_kind': 'text',
            'metadata_identity': json.dumps({'title': 'Al Ajrumiyyah'}),
            'metadata_classification': json.dumps({'language': 'Arabic'}),
        },
        format='multipart',
    )
    assert create_response.status_code == 201
    created_public_id = create_response.data['public_id']

    other_client = APIClient()
    login_response = other_client.post(
        '/api/v1/auth/login/',
        {'email': other_user.email, 'password': 'StrongPass123'},
        format='json',
    )
    other_client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['tokens']['access']}")

    list_response = other_client.get('/api/v1/library/books/')
    payload = list_response.data['results'] if isinstance(list_response.data, dict) else list_response.data
    assert all(item['public_id'] != str(created_public_id) for item in payload)


@pytest.mark.django_db
def test_ingestion_job_creation(authenticated_client, user):
    book = Book.objects.create(
        title='Text Book',
        visibility='public',
        public=True,
        uploaded_by=user,
    )
    book.files.create(
        file=SimpleUploadedFile('source.txt', b'Content for ingestion', content_type='text/plain'),
        file_kind='text',
        original_filename='source.txt',
        is_primary=True,
    )

    response = authenticated_client.post(
        '/api/v1/ingestion/jobs/',
        {'book_public_id': str(book.public_id), 'source_note': 'Initial upload'},
        format='json',
    )
    assert response.status_code == 201
    assert response.data['status'] in {'queued', 'processing', 'review_pending'}


@pytest.mark.django_db
def test_qa_returns_safe_response_when_no_sources(authenticated_client, user):
    response = authenticated_client.post(
        '/api/v1/qa/questions/',
        {'question': 'What is the ruling on a topic with no uploaded source?', 'scope': 'general'},
        format='json',
    )
    assert response.status_code == 201
    assert response.data['latest_answer']['verification_status'] == 'needs_review'
    assert 'Insufficient verified source support' in response.data['latest_answer']['direct_answer']


@pytest.mark.django_db
def test_provider_selection_hierarchy(user, institute):
    InstituteMembership.objects.create(user=user, institute=institute, role='student', is_active=True)
    AIProvider.objects.create(name='openrouter', scope='system', api_key='system-key', is_active=True, priority=1)
    AIProvider.objects.create(
        name='openrouter',
        scope='institute',
        api_key='institute-key',
        institute=institute,
        is_active=True,
        priority=5,
    )
    AIProvider.objects.create(
        name='openrouter',
        scope='user',
        api_key='user-key',
        user=user,
        is_active=True,
        priority=10,
    )

    resolved = resolve_provider('openrouter', user=user, institute=institute)
    assert resolved.scope == 'user'
    assert resolved.api_key == 'user-key'

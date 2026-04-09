from __future__ import annotations

from decimal import Decimal

from apps.analytics.services import track_event

from .models import Answer, Query, RetrievedSource
from .selectors import classify_question, retrieve_chunks, select_skill_pack


INSUFFICIENT_SUPPORT_MESSAGE = (
    'Insufficient verified source support was found in the current library scope. '
    'Please narrow the question to a specific book, topic, or passage, or request scholar review.'
)


def _source_reference_line(item):
    chunk = item['chunk']
    book_name = chunk.book.arabic_title or chunk.book.title
    if chunk.page_number:
        return f'{book_name}, p. {chunk.page_number}'
    return book_name


def _build_supported_sections(question: str, results):
    references = [_source_reference_line(item) for item in results[:3]]
    snippets = [item['chunk'].content[:280].strip().replace('\n', ' ') for item in results[:3]]
    direct_answer = 'Relevant source passages were found in: ' + '; '.join(references) + '.'
    explanation = '\n\n'.join(
        f'{index + 1}. {snippet}' for index, snippet in enumerate(snippets)
    )
    simplified = 'These passages point to the same area of study. Read the cited excerpts before relying on the answer.'
    examples = [
        {
            'type': 'source_excerpt',
            'text': snippet,
        }
        for snippet in snippets[:2]
    ]
    return direct_answer, explanation, simplified, examples


def generate_grounded_answer(*, user, question: str, language_pair='ar-en', scope='general', subject='', book_public_id=None, institute_public_id=None):
    classification = classify_question(question, scope, subject=subject)
    results = retrieve_chunks(
        user=user,
        question=question,
        scope=scope,
        book_public_id=book_public_id,
        institute_public_id=institute_public_id,
    )
    skill_pack = select_skill_pack(results, subject=classification.subject)

    query = Query.objects.create(
        user=user,
        question=question,
        language_pair=language_pair,
        detected_subject=classification.subject,
        detected_intent=classification.intent,
        sensitivity_level=classification.sensitivity,
        search_scope=classification.scope,
        verification_preference='source_grounded',
    )

    if not results:
        answer = Answer.objects.create(
            query=query,
            selected_skill_pack=skill_pack,
            direct_answer=INSUFFICIENT_SUPPORT_MESSAGE,
            detailed_explanation='No sufficiently matched book chunks were retrieved from the allowed library scope.',
            simplified_explanation='Try asking about a specific book, chapter, rule, or page.',
            generated_examples=[],
            verification_status='needs_review',
            confidence=Decimal('0.15'),
            related_topics=[classification.subject] if classification.subject else [],
            answer_provenance={'mode': 'db_retrieval', 'source_count': 0},
        )
    else:
        direct_answer, explanation, simplified, examples = _build_supported_sections(question, results)
        confidence_value = min(Decimal('0.95'), Decimal('0.45') + Decimal('0.10') * Decimal(len(results)))
        answer = Answer.objects.create(
            query=query,
            selected_skill_pack=skill_pack,
            direct_answer=direct_answer,
            detailed_explanation=explanation,
            simplified_explanation=simplified,
            generated_examples=examples,
            verification_status='source_grounded',
            confidence=confidence_value,
            related_topics=[classification.subject] if classification.subject else [],
            answer_provenance={
                'mode': 'db_retrieval',
                'source_count': len(results),
                'scope': scope,
            },
        )
        for item in results:
            chunk = item['chunk']
            RetrievedSource.objects.create(
                answer=answer,
                book=chunk.book,
                chunk=chunk,
                page_number=chunk.page_number,
                score=Decimal(str(min(item['score'] / 10, 0.9999))).quantize(Decimal('0.0001')),
                retrieval_reason='keyword_overlap',
            )

    query.response = {
        'answer_public_id': str(answer.public_id),
        'verification_status': answer.verification_status,
        'confidence': str(answer.confidence),
    }
    query.save(update_fields=['response', 'updated_at'])

    track_event(
        'qa_question_answered',
        user=user,
        payload={
            'query_public_id': str(query.public_id),
            'answer_public_id': str(answer.public_id),
            'verification_status': answer.verification_status,
            'scope': scope,
        },
    )
    return query

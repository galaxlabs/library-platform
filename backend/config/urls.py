from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views import RegisterView, LoginView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

from django.http import HttpResponse

admin.site.site_header = 'Maktaba Ilmiah'
admin.site.site_title = 'Maktaba Ilmiah Admin'
admin.site.index_title = 'Maktaba Ilmiah Control Panel'

urlpatterns = [
    # Backend root status page
    path('', lambda request: HttpResponse(
        'Maktaba Ilmiah backend is running. Use /admin/ or /api/v1/.'
    )),

    # Admin
    path('admin/', admin.site.urls),
    
    # API v1
    path('api/v1/', include([
        # Auth endpoints
        path('auth/register/', RegisterView.as_view(), name='register'),
        path('auth/login/', LoginView.as_view(), name='login'),
        path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        
        # Router for viewsets
        path('', include(router.urls)),
        
        # App-specific URLs
        path('institutes/', include('apps.institutes.urls')),
        path('scholars/', include('apps.scholars.urls')),
        path('library/', include('apps.library.urls')),
        path('ingestion/', include('apps.ingestion.urls')),
        path('knowledge/', include('apps.knowledge.urls')),
        path('skills/', include('apps.skills.urls')),
        path('qa/', include('apps.qa_engine.urls')),
        path('learning/', include('apps.learning.urls')),
        path('providers/', include('apps.ai_providers.urls')),
        path('analytics/', include('apps.analytics.urls')),
    ])),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

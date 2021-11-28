from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('facial_app.api.urls')),
    path('', include('facial_app.urls')),
    path('user/api/', include('user_app.api.urls')),
    path('user/', include('user_app.urls')),
    #Password Related Views
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # path('password_reset/', PasswordResetView.as_view(), name='password_reset_form'),
    # path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

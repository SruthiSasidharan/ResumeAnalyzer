"""
URL configuration for AI Career Guidance project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from career_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_resume, name='upload_resume'),
    path('analyze/<int:resume_id>/', views.analyze_resume, name='analyze_resume'),
    path('result/<int:resume_id>/', views.analysis_result, name='analysis_result'),
    path('jobs/', views.job_recommendations, name='job_recommendations'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

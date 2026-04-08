from django.contrib import admin
from .models import Skill, CareerRole, LearningResource, JobListing, Resume


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name']


@admin.register(CareerRole)
class CareerRoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = ['skill_name', 'resource_type', 'title', 'source']
    list_filter = ['resource_type', 'skill_name']


@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'role_slug', 'is_active']
    list_filter = ['role_slug', 'is_active']


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'uploaded_at', 'skill_score', 'career_readiness']

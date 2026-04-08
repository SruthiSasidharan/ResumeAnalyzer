"""
Database models for AI Career Guidance.
"""
from django.db import models
from .fields import JSONTextField


class Skill(models.Model):
    """Skills vocabulary for matching."""
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, blank=True)  # e.g., Programming, ML, Tools
    aliases = JSONTextField(default=list, blank=True)  # ["JS", "Javascript"]

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CareerRole(models.Model):
    """Job roles with required and optional skills."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    required_skills = JSONTextField(default=list)  # List of skill names
    optional_skills = JSONTextField(default=list)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class LearningResource(models.Model):
    """Learning resources per skill."""
    skill_name = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=20)  # course, certification, youtube, book
    title = models.CharField(max_length=300)
    url = models.URLField(blank=True)
    source = models.CharField(max_length=100, blank=True)  # Coursera, Udemy, etc.

    class Meta:
        ordering = ['skill_name', 'resource_type']

    def __str__(self):
        return f"{self.skill_name} - {self.title}"


class JobListing(models.Model):
    """Job listings from API or dataset."""
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    role_slug = models.CharField(max_length=100, blank=True)
    skills_required = JSONTextField(default=list)
    url = models.URLField(blank=True, max_length=512)
    posted_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-posted_date']

    def __str__(self):
        return f"{self.title} at {self.company}"


class Resume(models.Model):
    """Uploaded resume and analysis results."""
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # Extracted data
    raw_text = models.TextField(blank=True)
    skills = JSONTextField(default=list)  # Extracted skill names
    education = JSONTextField(default=list)
    experience = JSONTextField(default=list)
    # Analysis results
    predicted_roles = JSONTextField(default=list)  # [{"role": "...", "score": 0.8}]
    skill_gaps = JSONTextField(default=list)  # [{"skill": "...", "importance": "high"}]
    skill_score = models.FloatField(default=0.0)  # 0-100
    career_readiness = models.CharField(max_length=50, blank=True)  # Beginner, Intermediate, etc.
    learning_recommendations = JSONTextField(default=list)
    session_id = models.CharField(max_length=100, blank=True)  # For anonymous users

    def __str__(self):
        return f"Resume {self.id} - {self.file.name}"

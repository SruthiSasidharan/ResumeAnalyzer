"""
Views for AI Career Guidance - Dashboard, Upload, Analysis, Jobs.
"""
import os
import uuid
from django.shortcuts import render, redirect, get_object_or_404

from .models import Resume
from .services import ResumeAnalyzer, CareerPredictor, SkillGapDetector, LearningRecommender, JobRecommender


def dashboard(request):
    """Module 6: Dashboard - Skill score, career readiness, progress tracking."""
    return render(request, 'dashboard.html')


def upload_resume(request):
    """Upload resume (PDF/DOC)."""
    if request.method == 'POST':
        file = request.FILES.get('resume')
        if not file:
            return render(request, 'upload.html', {'error': 'Please select a file.'})
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in ('.pdf', '.doc', '.docx'):
            return render(request, 'upload.html', {'error': 'Only PDF and DOC/DOCX files are allowed.'})
        session_id = request.session.get('session_id') or str(uuid.uuid4())
        request.session['session_id'] = session_id
        resume = Resume.objects.create(file=file, session_id=session_id)
        return redirect('analyze_resume', resume_id=resume.id)
    return render(request, 'upload.html')


def analyze_resume(request, resume_id):
    """Run full analysis pipeline (Modules 1-5)."""
    resume = get_object_or_404(Resume, pk=resume_id)
    file_path = resume.file.path
    if not os.path.exists(file_path):
        return render(request, 'error.html', {'message': 'Resume file not found.'})

    analyzer = ResumeAnalyzer()
    analysis = analyzer.analyze(file_path)

    resume.raw_text = analysis['raw_text']
    resume.skills = analysis['skills']
    resume.education = analysis['education']
    resume.experience = analysis['experience']
    resume.save()

    predictor = CareerPredictor()
    predictions = predictor.predict(resume.skills)
    resume.predicted_roles = predictions

    gap_detector = SkillGapDetector()
    gap_result = gap_detector.detect(resume.skills)
    resume.skill_gaps = gap_result['gaps']
    resume.skill_score = gap_result['skill_score']
    resume.career_readiness = gap_result['career_readiness']

    learner = LearningRecommender()
    missing_skills = [g['skill'] for g in gap_result['gaps'][:10]]
    resume.learning_recommendations = learner.recommend(missing_skills)
    resume.save()

    return redirect('analysis_result', resume_id=resume.id)


def analysis_result(request, resume_id):
    """Display full analysis result - Dashboard view."""
    resume = get_object_or_404(Resume, pk=resume_id)
    job_recommender = JobRecommender()
    top_role = resume.predicted_roles[0]['slug'] if resume.predicted_roles else None
    jobs = job_recommender.recommend(role_slug=top_role, limit=8)

    context = {
        'resume': resume,
        'jobs': jobs,
    }
    return render(request, 'result.html', context)


def job_recommendations(request):
    """Job listings page."""
    role = request.GET.get('role', '')
    job_recommender = JobRecommender()
    jobs = job_recommender.recommend(role_name=role, role_slug=role, limit=20)
    return render(request, 'jobs.html', {'jobs': jobs, 'role_filter': role})

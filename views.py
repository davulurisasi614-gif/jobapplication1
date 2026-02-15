from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from .models import Job, Application

def home(request):
    """Display all available jobs"""
    try:
        jobs = Job.objects.all().order_by('-posted_on')
        return render(request, 'home.html', {'jobs': jobs})
    except Exception as e:
        messages.error(request, 'Error loading jobs. Please try again later.')
        return render(request, 'home.html', {'jobs': []})


@login_required(login_url='admin:login')
def post_job(request):
    """Post a new job listing"""
    if request.method == 'POST':
        try:
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            location = request.POST.get('location', '').strip()
            
            if not all([title, description, location]):
                messages.error(request, 'All fields are required.')
                return render(request, 'post_job.html')
            
            Job.objects.create(
                employer=request.user,
                title=title,
                description=description,
                location=location
            )
            messages.success(request, 'Job posted successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error posting job: {str(e)}')
            return render(request, 'post_job.html')
    
    return render(request, 'post_job.html')


@login_required(login_url='admin:login')
def apply_job(request, job_id):
    """Apply for a specific job"""
    job = get_object_or_404(Job, id=job_id)
    
    if request.method == 'POST':
        try:
            resume = request.FILES.get('resume')
            if not resume:
                messages.error(request, 'Please upload a resume.')
                return render(request, 'apply_job.html', {'job': job})
            
            # Check if user already applied
            existing_application = Application.objects.filter(
                job=job, 
                applicant=request.user
            ).exists()
            
            if existing_application:
                messages.warning(request, 'You have already applied for this job.')
                return render(request, 'apply_job.html', {'job': job})
            
            Application.objects.create(
                job=job,
                applicant=request.user,
                resume=resume
            )
            messages.success(request, 'Application submitted successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error submitting application: {str(e)}')
            return render(request, 'apply_job.html', {'job': job})
    
    return render(request, 'apply_job.html', {'job': job})

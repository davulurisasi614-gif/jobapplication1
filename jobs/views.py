from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User   # ✅ REQUIRED

from .models import Job, Application


# ================= HOME =================
def home(request):
    jobs = Job.objects.all().order_by('-posted_on')
    return render(request, 'home.html', {'jobs': jobs})


# ================= SIGNUP =================
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not all([username, email, password1, password2]):
            messages.error(request, 'All fields are required.')
            return render(request, 'signup.html')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'signup.html')

        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, 'Account created successfully. Please login.')
        return redirect('login')

    return render(request, 'signup.html')


# ================= LOGIN =================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('login')


# ================= POST JOB =================
@login_required
def post_job(request):
    if request.method == 'POST':
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

    return render(request, 'post_job.html')


# ================= APPLY JOB =================
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        resume = request.FILES.get('resume')

        if not resume:
            messages.error(request, 'Please upload a resume.')
            return render(request, 'apply_job.html', {'job': job})

        if Application.objects.filter(job=job, applicant=request.user).exists():
            messages.warning(request, 'You have already applied for this job.')
            return render(request, 'apply_job.html', {'job': job})

        Application.objects.create(
            job=job,
            applicant=request.user,
            resume=resume
        )

        messages.success(request, 'Application submitted successfully!')
        return redirect('home')

    return render(request, 'apply_job.html', {'job': job})

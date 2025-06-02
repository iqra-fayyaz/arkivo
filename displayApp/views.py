from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django .contrib import messages
from .forms import SignupForm, SigninForm, ProjectSubmissionForm, EditProfileForm
from .models import User, Project, Comment, Grade
from django.db.models.functions import ExtractYear
from django.views.decorators.http import require_POST
import random

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('/signin/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)    
                return redirect('/home/')
            else:
                print("DEBUG: Authentication Failed")
                return render(request, 'signin.html', {'form': form, 'error': 'Invalid username or password.'})
    else:
        form = SigninForm()
    return render(request, 'signin.html', {'form': form})


@login_required
def home(request):
    projects = Project.objects.select_related('student_id').order_by('-created_at')
    #projects = Project.objects.all().order_by('-created_at')  # All submitted projects
    status_choices = Project.STATUS_CHOICES  # :contentReference[oaicite:0]{index=0}
    dept_choices = User.Department_CHOICES   # :contentReference[oaicite:1]{index=1}
    category_choices = Project.PROJECT_CATEGORIES  # :contentReference[oaicite:2]{index=2}
    years_qs = (projects
                .annotate(year=ExtractYear('created_at'))
                .values_list('year', flat=True)
                .distinct()
                .order_by('-year'))
    year_list = list(years_qs)

    return render(request, 'home.html', {
        'projects': projects,
        'status_choices': status_choices,
        'dept_choices': dept_choices,
        'category_choices': category_choices,
        'year_list': year_list,
        })


def index(request):
    return render(request, 'index.html')


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'project_view.html', {'project': project})


@login_required
def myproject(request):
    project = Project.objects.filter(student_id = request.user).first()  # Get the first project for the logged-in user
    comments = project and Comment.objects.filter(project_id=project).order_by('created_at') if project else []
    
    return render(request, 'myproject.html', {
        'project': project,
        'comments': comments,
        'user_role': request.user.role
    })


@require_POST
@login_required
def add_comment(request, project_id):
    text = request.POST.get("comment", "").strip()
    if text:
        project = get_object_or_404(Project, pk=project_id)
        Comment.objects.create(
            comment=text,
            user_id=request.user,
            project_id=project
        )
    return redirect('myproject')


@login_required
def profile(request):
    user = request.user
    # counts for activity summary
    submissions_count = Project.objects.filter(student_id=user).count()
    comments_count    = Comment.objects.filter(user_id=user).count()
    project = Project.objects.filter(student_id = request.user).first()
    return render(request, 'profile.html' , {
        'project': project,
        'user_role': request.user.role,
        'submissions_count': submissions_count,
        'comments_count': comments_count,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        else:
            print(form.errors)
            messages.error(request, 'Error updating profile. Please check the form.')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {
        'form': form
    })


def mock_turnitin_score():
    return round(random.uniform(0, 30), 2)


@login_required
def submit_project(request):
    if Project.objects.filter(student_id=request.user).exists():
        messages.warning(request, "You’ve already submitted a project. You cannot submit more than one.")
        return redirect('myproject')    
    
    if request.method == 'POST':
        form = ProjectSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            similarity_score = mock_turnitin_score()
            if similarity_score < 20:
                project = form.save(commit=False)
                project.student_id = request.user  # Relates to the logged-in student
                project.plagiarism_score = similarity_score
                project.save()
                messages.success(request, f'Project submitted successfully. Similarity score: {similarity_score}%')
                return redirect('myproject')
            else:
                messages.error(request, f'Submission failed. Similarity score too high: {similarity_score}%')
    else:
        form = ProjectSubmissionForm()
    return render(request, 'submit_project.html', {'form': form})


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id, student_id=request.user)
    if request.method == 'POST':
        form = ProjectSubmissionForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('myproject')
        else:
            messages.error(request, 'There was an error updating the project.')
    else:
        form = ProjectSubmissionForm(instance=project)

    return render(request, 'edit_project.html', {'form': form})

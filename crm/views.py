from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Task, Project, TaskLog

# 👤 USER AUTHENTICATION


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# 🏠 MAIN DASHBOARD


@login_required
def dashboard(request):
    projects = Project.objects.all()
    tasks = Task.objects.all()

    todo_count = tasks.filter(status__icontains='do').count()
    progress_count = tasks.filter(status__icontains='progress').count()
    done_count = tasks.filter(status__icontains='done').count()

    return render(request, 'crm/dashboard.html', {
        'projects': projects,
        'tasks': tasks.order_by('-id')[:3],
        'todo_count': todo_count,
        'progress_count': progress_count,
        'done_count': done_count,
    })

# 📋 PROJECT VIEWS


@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'crm/project_list.html', {'projects': projects})


@login_required
def project_detail(request, id):
    # Updated to fetch tasks associated with this specific project
    project = get_object_or_404(Project, id=id)
    tasks = Task.objects.filter(project=project)
    return render(request, 'crm/project_detail.html', {
        'project': project,
        'tasks': tasks
    })


@login_required
def project_create(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        Project.objects.create(name=name, description=description)
        return redirect('project_list')
    return render(request, 'crm/project_form.html')

# 📝 TASK VIEWS


@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'crm/task_list.html', {'tasks': tasks})


@login_required
def task_detail(request, id):
    task = get_object_or_404(Task, id=id)
    return render(request, 'crm/task_detail.html', {'task': task})


@login_required
def task_create(request):
    if request.method == "POST":
        task = Task.objects.create(
            title=request.POST.get('title'),
            project_id=request.POST.get('project'),
            assigned_to_id=request.POST.get('assigned_to'),
            status=request.POST.get('status'),
            description=request.POST.get('description')
        )
        return redirect('task_detail', id=task.id)

    projects = Project.objects.all()
    users = User.objects.all()
    return render(request, 'crm/task_form.html', {'projects': projects, 'users': users})


@login_required
def task_update(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        task.title = request.POST.get('title')
        task.project_id = request.POST.get('project')
        task.assigned_to_id = request.POST.get('assigned_to')
        task.status = request.POST.get('status')
        task.save()

        note = request.POST.get('description')
        if note:
            TaskLog.objects.create(task=task, note=note)

        return redirect('task_detail', id=task.id)

    projects = Project.objects.all()
    users = User.objects.all()
    return render(request, 'crm/task_form.html', {
        'task': task,
        'projects': projects,
        'users': users
    })


@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        task.delete()
        return redirect('task_list')
    return render(request, 'crm/confirm_delete.html', {'task': task})

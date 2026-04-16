from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
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

    # ✅ Admin sees all, users see only theirs
    if request.user.is_superuser:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=request.user)

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
    project = get_object_or_404(Project, id=id)

    # ✅ Filter tasks per user unless admin
    if request.user.is_superuser:
        tasks = Task.objects.filter(project=project)
    else:
        tasks = Task.objects.filter(project=project, assigned_to=request.user)

    return render(request, 'crm/project_detail.html', {
        'project': project,
        'tasks': tasks
    })


@login_required
def project_create(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')

        Project.objects.create(
            name=name,
            description=description,
            created_by=request.user
        )
        return redirect('project_list')

    return render(request, 'crm/project_form.html')


# 📝 TASK VIEWS
@login_required
def task_list(request):

    # ✅ Admin vs User filtering
    if request.user.is_superuser:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=request.user)

    return render(request, 'crm/task_list.html', {'tasks': tasks})


@login_required
def task_detail(request, id):

    # ✅ Secure access (NO URL hacking)
    if request.user.is_superuser:
        task = get_object_or_404(Task, id=id)
    else:
        task = get_object_or_404(Task, id=id, assigned_to=request.user)

    logs = task.logs.all()

    return render(request, 'crm/task_detail.html', {
        'task': task,
        'logs': logs
    })


@login_required
def task_create(request):
    if request.method == "POST":
        assigned_id = request.POST.get('assigned_to')

        if assigned_id:
            assigned_user = User.objects.get(id=assigned_id)
        else:
            assigned_user = request.user

        description = request.POST.get('description')

        task = Task.objects.create(
            title=request.POST.get('title'),
            project_id=request.POST.get('project'),
            assigned_to=assigned_user,
            status=request.POST.get('status'),
            description=description
        )

        # ✅ Initial log
        if description:
            TaskLog.objects.create(
                task=task,
                note=description
            )

        return redirect('task_detail', id=task.id)

    projects = Project.objects.all()
    users = User.objects.all()

    return render(request, 'crm/task_form.html', {
        'projects': projects,
        'users': users
    })


@login_required
def task_update(request, id):

    # ✅ Secure edit access
    if request.user.is_superuser:
        task = get_object_or_404(Task, id=id)
    else:
        task = get_object_or_404(Task, id=id, assigned_to=request.user)

    if request.method == "POST":
        task.title = request.POST.get('title')
        task.project_id = request.POST.get('project')
        task.assigned_to_id = request.POST.get('assigned_to')
        task.status = request.POST.get('status')
        task.save()

        note = request.POST.get('description')

        if note:
            TaskLog.objects.create(
                task=task,
                note=note
            )

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

    # ✅ Secure delete
    if request.user.is_superuser:
        task = get_object_or_404(Task, id=id)
    else:
        task = get_object_or_404(Task, id=id, assigned_to=request.user)

    if request.method == "POST":
        task.delete()
        return redirect('task_list')

    return render(request, 'crm/confirm_delete.html', {'task': task})


# 🛠️ EMERGENCY LOGIN FIX
def create_admin_emergency(request):
    username = 'ruan_admin'
    password = 'ChangeThisPassword123!'

    user, created = User.objects.get_or_create(username=username)
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()

    if created:
        return HttpResponse(f"✅ Created superuser: {username}")
    return HttpResponse(f"🔄 Reset password for: {username}")
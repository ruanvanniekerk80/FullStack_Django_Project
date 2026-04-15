from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Main Dashboard
    path('', views.dashboard, name='dashboard'),

    # 📋 Projects
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:id>/', views.project_detail, name='project_detail'),
    path('projects/create/', views.project_create, name='project_create'),

    # 📝 Tasks
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:id>/', views.task_detail, name='task_detail'),
    path('tasks/create/', views.task_create, name='task_create'),

    # ✏️ EDIT TASK
    # Updated 'name' to 'task_update' to match your template tags
    path('tasks/update/<int:id>/', views.task_update, name='task_update'),

    # 🗑 DELETE TASK
    path('tasks/delete/<int:id>/', views.delete_task, name='delete_task'),

    # 👤 User Management
    path('signup/', views.SignUpView.as_view(), name='signup'),

    path('emergency-setup-admin/', views.create_admin_emergency),
]

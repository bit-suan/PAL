from django.urls import path
from . import views

urlpatterns = [
    # Template views
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('logout-confirm/', views.logout_confirm_view, name='logout-confirm'),
    
    # Web views for managing data
    path('manage-todos/', views.manage_todos, name='manage-todos'),
    path('add-log-entry/', views.add_log_entry, name='add-log-entry'),
    path('detailed-stats/', views.detailed_stats, name='detailed-stats'),  # Make sure this line exists
    path('profile-settings/', views.profile_settings, name='profile-settings'),
    
    # AJAX endpoints
    path('toggle-todo/<int:todo_id>/', views.toggle_todo, name='toggle-todo'),
    path('delete-todo/<int:todo_id>/', views.delete_todo, name='delete-todo'),
    
    # API endpoints (if you want to keep them)
    path('api/stats/', views.productivity_stats_view, name='api-stats'),
]
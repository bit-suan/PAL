# REST Framework imports
from rest_framework import generics, status, viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import json

# Local imports
from .models import Todo, Log, UserProfile  
from .serializers import RegisterSerializer, UserSerializer, LogSerializer, TodoSerializer, UserProfileSerializer
from .forms import TodoForm, LogForm, ProfileForm, CustomUserCreationForm

User = get_user_model()

# ---------------------- Template Views ----------------------

def home_view(request):
    """Home page view"""
    return render(request, 'core/home.html')

@login_required
def dashboard_view(request):
    """Main dashboard view"""
    user = request.user
    
    # Get some basic stats
    completed_todos = Todo.objects.filter(user=user, status='completed').count()
    
    # Get recent activity (simplified)
    today = timezone.now().date()
    start_date = today - timedelta(days=7)  # Last 7 days
    logs = Log.objects.filter(user=user, date__gte=start_date)
    log_dates = set(log.date.date() for log in logs)
    
    daily_streak = []
    for i in range(7):
        check_day = today - timedelta(days=i)
        daily_streak.append({
            "date": check_day,
            "activity": check_day in log_dates
        })
    
    context = {
        'user': user,
        'completed_todos': completed_todos,
        'current_streak': len([d for d in daily_streak if d['activity']]),
        'daily_streak': daily_streak,
    }
    
    return render(request, 'core/dashboard.html', context)

def signup_view(request):
    """Signup form view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def productivity_stats_view(request):
    """Template-based productivity stats view"""
    user = request.user
    completed_todos = Todo.objects.filter(user=user, status='completed').count()
    today = timezone.now().date()
    start_date = today - timedelta(days=30)
    logs = Log.objects.filter(user=user, date__gte=start_date)
    log_dates = set(log.date.date() for log in logs)
    
    streak = 0
    daily_streak = []
    for i in range(30):
        check_day = today - timedelta(days=i)
        if check_day in log_dates:
            streak += 1
            daily_streak.append({"date": check_day, "activity": True})
        else:
            daily_streak.append({"date": check_day, "activity": False})
    
    return render(request, 'core/stats.html', {
        'user': user,
        'completed_todos': completed_todos,
        'current_streak': streak,
        'daily_streak': daily_streak,
    })

@login_required
def logout_view(request):
    """Custom logout view that handles both GET and POST"""
    if request.method == 'POST':
        logout(request)
        return render(request, 'registration/logged_out.html')
    else:
        # Show logout confirmation page for GET requests
        return render(request, 'registration/logout_confirm.html')

def logout_confirm_view(request):
    """Simple logout that works with GET requests"""
    logout(request)
    return render(request, 'registration/logged_out.html')

@login_required
def manage_todos(request):
    """Web view for managing todos"""
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Todo created successfully!')
            return redirect('manage-todos')
    else:
        form = TodoForm()
    
    todos = Todo.objects.filter(user=request.user).order_by('-id')
    return render(request, 'core/manage_todos.html', {
        'todos': todos,
        'form': form
    })

@login_required
def add_log_entry(request):
    """Web view for adding log entries"""
    if request.method == 'POST':
        form = LogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, 'Log entry added successfully!')
            return redirect('add-log-entry')
    else:
        form = LogForm()
    
    # FIXED: Use 'date' instead of 'timestamp'
    recent_logs = Log.objects.filter(user=request.user).order_by('-date')[:10]
    return render(request, 'core/add_log.html', {
        'form': form,
        'recent_logs': recent_logs
    })

@login_required
def detailed_stats(request):
    """Web view for detailed statistics"""
    user_todos = Todo.objects.filter(user=request.user)
    user_logs = Log.objects.filter(user=request.user)
    
    # Calculate todo statistics
    total_todos = user_todos.count()
    completed_todos = user_todos.filter(status='completed').count()
    pending_todos = user_todos.filter(status='pending').count()
    
    # Calculate completion rate
    completion_rate = (completed_todos / total_todos * 100) if total_todos > 0 else 0
    
    # Get todos created this week
    week_ago = timezone.now() - timedelta(days=7)
    todos_this_week = user_todos.count()  # Simplified for now
    
    stats = {
        'total_todos': total_todos,
        'completed_todos': completed_todos,
        'pending_todos': pending_todos,
        'completion_rate': completion_rate,
        'total_logs': user_logs.count(),
        'recent_logs': user_logs.order_by('-date')[:5],  # FIXED: Use 'date' instead of 'timestamp'
        'recent_todos': user_todos.order_by('-id')[:5],
        'todos_this_week': todos_this_week,
    }
    
    return render(request, 'core/detailed_stats.html', stats)

@login_required
def profile_settings(request):
    """Web view for profile settings"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile-settings')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'core/profile_settings.html', {
        'form': form,
        'profile': profile
    })

@login_required
def toggle_todo(request, todo_id):
    """AJAX view to toggle todo completion"""
    if request.method == 'POST':
        todo = get_object_or_404(Todo, id=todo_id, user=request.user)
        todo.status = 'completed' if todo.status == 'pending' else 'pending'
        todo.save()
        return JsonResponse({
            'success': True,
            'completed': todo.status == 'completed',
            'message': f'Todo {"completed" if todo.status == "completed" else "reopened"}!'
        })
    return JsonResponse({'success': False})

@login_required
def delete_todo(request, todo_id):
    """AJAX view to delete todo"""
    if request.method == 'POST':
        todo = get_object_or_404(Todo, id=todo_id, user=request.user)
        todo.delete()
        return JsonResponse({
            'success': True,
            'message': 'Todo deleted successfully!'
        })
    return JsonResponse({'success': False})

# ---------------------- API Views ----------------------

class RegisterView(generics.CreateAPIView):
    """API endpoint for user registration"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_201_CREATED)

# ---------------------- User Profile ViewSet ----------------------

class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user profiles"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ---------------------- Log ViewSet ----------------------

class LogViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user logs"""
    serializer_class = LogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Log.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this log.")
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this log.")
        instance.delete()

# ---------------------- Todo ViewSet ----------------------

class TodoViewSet(viewsets.ModelViewSet):
    """ViewSet for managing todos with enhanced functionality"""
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['task']
    ordering_fields = ['due_date', 'status']
    
    def get_queryset(self):
        queryset = Todo.objects.filter(user=self.request.user)
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this todo.")
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this todo.")
        instance.delete()

# ---------------------- Productivity Stats API ----------------------

class ProductivityStatsView(APIView):
    """API endpoint for productivity statistics"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        completed_todos = Todo.objects.filter(user=user, status='completed').count()
        today = timezone.now().date()
        start_date = today - timedelta(days=30)
        logs = Log.objects.filter(user=user, date__gte=start_date)
        log_dates = set(log.date.date() for log in logs)
        
        streak = 0
        daily_streak = []
        for i in range(30):
            check_day = today - timedelta(days=i)
            if check_day in log_dates:
                streak += 1
                daily_streak.append({"date": check_day, "activity": True})
            else:
                daily_streak.append({"date": check_day, "activity": False})
        
        return Response({
            'completed_todos': completed_todos,
            'current_streak': streak,
            'daily_streak': daily_streak,
        })

# ---------------------- Todo Summary API ----------------------

class TodoSummaryView(APIView):
    """API endpoint for todo summary statistics"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        todos = Todo.objects.filter(user=user)
        total = todos.count()
        completed = todos.filter(status='completed').count()
        pending = todos.filter(status='pending').count()
        overdue = todos.filter(due_date__lt=timezone.now().date(), status='pending').count()
        upcoming = todos.filter(due_date__gt=timezone.now().date(), status='pending').count()
        progress = (completed / total * 100) if total > 0 else 0
        
        return Response({
            'total_todos': total,
            'completed': completed,
            'pending': pending,
            'overdue': overdue,
            'upcoming': upcoming,
            'progress_percentage': round(progress, 2)
        })
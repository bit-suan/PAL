from rest_framework import generics, status, viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Log, Todo
from .serializers import RegisterSerializer, UserSerializer, LogSerializer, TodoSerializer
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


User = get_user_model()
# ---------------------- Auth & Registration ----------------------

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# ---------------------- Auth & Registration ----------------------
class RegisterView(generics.CreateAPIView):
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

# ---------------------- Log ViewSet ----------------------
class LogViewSet(viewsets.ModelViewSet):
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
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['task']
    ordering_fields = ['due_date', 'status']

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        todos = Todo.objects.filter(user=user)

        total = todos.count()
        completed = todos.filter(status='completed').count()
        pending = todos.filter(status='pending').count()
        overdue = todos.filter(due_date__lt=timezone.now(), status='pending').count()
        upcoming = todos.filter(due_date__gt=timezone.now(), status='pending').count()

        progress = (completed / total * 100) if total > 0 else 0

        return Response({
            'total_todos': total,
            'completed': completed,
            'pending': pending,
            'overdue': overdue,
            'upcoming': upcoming,
            'progress_percentage': round(progress, 2)
        })

# ---------------------- Template-Based Dashboard View ----------------------
@login_required
def productivity_stats_view(request):
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

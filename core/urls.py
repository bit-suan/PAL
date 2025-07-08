from django.urls import path, include
from .views import (
    RegisterView,
    LogViewSet,
    TodoViewSet,
    ProductivityStatsView,
    TodoSummaryView,
    signup_view,
    productivity_stats_view,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'logs', LogViewSet, basename='log')
router.register(r'todos', TodoViewSet, basename='todo')

urlpatterns = [
    # Authentication and Registration
    path('register/', RegisterView.as_view(), name='register'),
    path('signup/', signup_view, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Stats and Dashboard
    path('stats/productivity/', ProductivityStatsView.as_view(), name='productivity-stats'),
    path('stats/todos/', TodoSummaryView.as_view(), name='todo-summary'),
    path('dashboard/', productivity_stats_view, name='productivity-dashboard'),

    # DRF ViewSets (CRUD logs & todos)
    path('', include(router.urls)),
]

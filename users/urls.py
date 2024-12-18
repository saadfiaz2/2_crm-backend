from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cms.views import LeadByLeadGenManagerView
from .views import *

router = DefaultRouter()
router.register(r'education', EducationViewSet, basename='education')
router.register(r'work', WorkViewSet, basename='work')

urlpatterns = [
    path('check-credentials/', CheckCredentialsView.as_view(), name='check-credentials'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('current-user/', current_user_view, name='current_user'),
    path('password-reset/', PasswordResetView, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('users/by-role/', UserByRoleAPIView.as_view(), name='user-by-role'),
    path('leads/lead-gen-manager/<int:lead_gen_manager_id>/', LeadByLeadGenManagerView.as_view(),
         name='lead_by_lead_gen_manager'),

    path('', include(router.urls)),
]

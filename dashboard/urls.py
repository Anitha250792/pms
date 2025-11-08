from django.urls import path
from . import views

app_name = 'dashboard' 

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('member/<int:user_id>/', views.member_dashboard_view, name='member_dashboard'),
]

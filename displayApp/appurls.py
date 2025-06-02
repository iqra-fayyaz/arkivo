from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('home/', views.home, name='home'),
    path('myproject/', views.myproject, name='myproject'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('index/', views.index, name='index'),
    path('submit_project/', views.submit_project, name='submit_project'),
    path('project/<int:project_id>/add_comment/', views.add_comment, name='add_comment'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/edit/<int:project_id>/', views.edit_project, name='edit_project'),
    path('logout/', auth_views.LogoutView.as_view(next_page='signin'), name='logout'),
]
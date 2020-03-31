from django.urls import path
from django.contrib.auth import views as auth_views

from core.views import home, subcategory, category, organization, organizations, about_project, register, profile, \
    edit_profile

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('profile/<int:pk>/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),

    path('', home, name='home'),
    path('categories/<str:category_name>/', category, name='category'),
    path('subcategory/<str:subcategory_name>/', subcategory, name='subcategory'),
    path('organizations/', organizations, name='organizations'),
    path('organizations/<str:org_name>/', organization, name='organization'),

    path('about_project/', about_project, name='about-project'),
]

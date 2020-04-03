from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import cache_page

from core.views import home, subcategory, category, organization, organizations, about_project, register, profile, \
    edit_profile

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('profile/<int:pk>/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),

    path('', cache_page(60 * 5)(home), name='home'),
    path('categories/<str:category_name>/', cache_page(60 * 5)(category), name='category'),
    path('subcategory/<str:subcategory_name>/', cache_page(60 * 5)(subcategory), name='subcategory'),
    path('organizations/', cache_page(60 * 5)(organizations), name='organizations'),
    path('organizations/<str:org_name>/', organization, name='organization'),

    path('about_project/', about_project, name='about-project'),
]

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login

from core.forms import UserRegistrationForm, EditProfileForm
from core.models import Category, Subcategory, Organization, Profile


def home(request):
    if request.method == 'GET':
        all_categories = Category.objects.all()
        context = {
            'all_categories': all_categories
        }
        return render(request, 'core/home.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'GET':
        form = UserRegistrationForm()
    else:
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            authenticated_user = authenticate(
                username=username, password=raw_password,
            )
            login(request, authenticated_user)
            return redirect('home')

    context = {'form': form}
    return render(request, 'core/register.html', context)


def profile(request, pk):
    profile_user = get_object_or_404(User, id=pk)
    target_profile = Profile.objects.get(user=profile_user)
    context = {
        'prof': target_profile,
    }
    return render(request, 'core/profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    target_user = User.objects.get(id=request.user.id)
    target_profile = target_user.profile
    if request.method == 'POST':
        edit_profile_form = EditProfileForm(request.POST, request.FILES)

        if edit_profile_form.is_valid():
            data = edit_profile_form.cleaned_data

            parameters = {
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'email': data.get('email')
            }
            save_cur_user_info(target_user, parameters)

            image = data.get('image')
            save_cur_prof_info(target_profile, image)
            return redirect(reverse('profile', args=[request.user.id]))
        else:
            return redirect(reverse('profile', args=[request.user.id]))

    else:
        edit_profile_form = EditProfileForm({
            'first_name': target_user.first_name,
            'last_name': target_user.last_name,
            'email': target_user.email,
        })
        context = {
            'edit_profile_form': edit_profile_form,
        }
        return render(request, 'core/edit_profile.html', context)


def save_cur_user_info(target_user, parameters):
    for field, value in parameters.items():
        setattr(target_user, field, value)
    target_user.save()


def save_cur_prof_info(target_profile, image):
    if image:
        target_profile.image = image
    target_profile.save()


def category(request, category_name):
    context = {}
    if request.method == 'GET':
        current_category = Category.objects.get(name=category_name)
        context['target_subcategories'] = current_category.subcategories.all()
        return render(request, 'core/category.html', context)


def subcategory(request, subcategory_name):
    context = {}
    if request.method == 'GET':
        current_subcategory = Subcategory.objects.get(name=subcategory_name)
        context['subcategory'] = current_subcategory
        return render(request, 'core/subcategory.html', context)


def organization(request, org_name):
    if request.method == 'GET':
        target_organization = Organization.objects.get(name=org_name)
        context = {
            'target_organization': target_organization
        }
        return render(request, 'core/organization.html', context)


def organizations(request):
    all_organizations = Organization.objects.all()
    context = {
        'all_organizations': all_organizations
    }
    return render(request, 'core/organizations.html', context)


def about_project(request):
    return render(request, 'core/about_project.html')

from django.core.paginator import Paginator
from django.shortcuts import redirect

from core.forms import CreatePostForm
from core.models import Post


def save_cur_user_info(target_user, parameters):
    for field, value in parameters.items():
        setattr(target_user, field, value)
    target_user.save()


def save_cur_prof_info(target_profile, image):
    if image:
        target_profile.image = image
    target_profile.save()


def paginate(request, objects, num_of_elements):
    objects = Paginator(objects, num_of_elements)
    page = request.GET.get('page')
    objects = objects.get_page(page)
    return objects


def create_post(request, target_profile):
    create_post_form = CreatePostForm(request.POST or None)
    if create_post_form.is_valid():
        post_text = create_post_form.cleaned_data['text']
        post = Post.objects.create(author=request.user.profile, text=post_text)
        post.save()
        return redirect('profile', pk=target_profile.pk)

from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.shortcuts import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Organization(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=700, blank=True, null=True)
    owner = models.ForeignKey(Profile, related_name='organizations', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class PhoneNumber(models.Model):
    organization = models.ForeignKey(Organization, related_name='phone_numbers', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.organization.name} - {self.phone_number}'


class Address(models.Model):
    organization = models.ForeignKey(Organization, related_name='addresses', on_delete=models.CASCADE)
    address = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.organization.name} - {self.address}'


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=150)
    parent_category = models.ForeignKey(Category, related_name='subcategories', blank=True, null=True,
                                        on_delete=models.SET_NULL)
    organizations = models.ManyToManyField(Organization, related_name='subcategories', blank=True)
    middle_layer = models.ForeignKey('self', blank=True, related_name='parent_layer', null=True,
                                     on_delete=models.SET_NULL)

    def __str__(self):
        string = f'{self.name} - {self.parent_category} - {self.middle_layer}' if self.middle_layer else f'{self.name} - {self.parent_category}'
        return string


class Tag(models.Model):
    name = models.CharField(max_length=80)
    organizations = models.ManyToManyField(Organization, related_name='tags', blank=True)
    subcategories = models.ManyToManyField(Subcategory, related_name='tags', blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Profile, related_name='posts', null=True, on_delete=models.SET_NULL,
                               verbose_name="author's profile")
    text = models.CharField(max_length=1400)
    date_posted = models.DateTimeField(auto_now_add=True)

    def delete_post(self):
        return reverse('delete_post', kwargs={
            'pk': self.pk
        })

    def get_authors_name(self):
        return self.author.user.username

    def __str__(self):
        return f'By {self.author.user.username} - {self.text[:10]}'

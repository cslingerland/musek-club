from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse

# Create your models here.

CLUB_TYPE_CHOICES = (
    ('songs', 'Songs'),
    ('albums', 'Albums')
)

class Club(models.Model):
    name = models.CharField(
        verbose_name='name',
        max_length=50
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=50,
        unique=True
    )
    tagline = models.CharField(
        verbose_name='tagline',
        max_length=60, 
        blank=True,
        null=True
    )
    club_type = models.CharField(
        verbose_name='club type',
        max_length=20,
        choices=CLUB_TYPE_CHOICES,
        default='songs'
    )
    members = models.ManyToManyField(User)
    create_date = models.DateTimeField(
        verbose_name='date created'
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("clubs:club", args=[self.slug])


class Pick(models.Model):
    name = models.CharField(
        verbose_name='name',
        max_length=50
    )
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    url = models.URLField(
        verbose_name='url'
    )
    reason = models.CharField(
        verbose_name='reason',
        max_length=250
    )
    active = models.BooleanField(default=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True
    )
    created = models.DateTimeField(
        verbose_name='date created'
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("clubs:club", args=[self.slug])
    
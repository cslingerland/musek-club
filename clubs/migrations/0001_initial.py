# Generated by Django 5.1.4 on 2024-12-12 01:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('tagline', models.CharField(blank=True, max_length=60, null=True, verbose_name='tagline')),
                ('club_type', models.CharField(choices=[('songs', 'Songs'), ('albums', 'Albums')], default='songs', max_length=20, verbose_name='club type')),
                ('create_date', models.DateTimeField(verbose_name='date created')),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
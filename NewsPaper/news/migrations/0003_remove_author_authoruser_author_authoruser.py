# Generated by Django 4.0.2 on 2022-03-26 15:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0002_usercategory_category_subscribers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='authorUser',
        ),
        migrations.AddField(
            model_name='author',
            name='authorUser',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]

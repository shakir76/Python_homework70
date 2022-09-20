# Generated by Django 4.0.5 on 2022-09-20 07:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0016_alter_article_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='article', to=settings.AUTH_USER_MODEL),
        ),
    ]

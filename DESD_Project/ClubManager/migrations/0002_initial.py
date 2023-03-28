# Generated by Django 3.2.16 on 2023-03-28 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ClubManager', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UWEFlix', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubrepprofile',
            name='clubID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='UWEFlix.club'),
        ),
        migrations.AddField(
            model_name='clubrepprofile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

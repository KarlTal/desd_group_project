# Generated by Django 4.1.7 on 2023-04-02 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0002_alter_club_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='club',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UWEFlix.club'),
        ),
    ]

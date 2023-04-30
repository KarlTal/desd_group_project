# Generated by Django 3.2.16 on 2023-04-28 08:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0002_booking_pending_cancel'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='has_been_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='AccountStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookings', models.ManyToManyField(to='UWEFlix.Booking')),
                ('user_obj', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

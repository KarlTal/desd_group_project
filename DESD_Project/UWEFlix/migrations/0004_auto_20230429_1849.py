# Generated by Django 3.2.16 on 2023-04-29 17:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0003_auto_20230428_0928'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.EmailField(max_length=254, null=True)),
                ('type', models.CharField(choices=[('Debit', 'Debit'), ('Credit', 'Credit')], max_length=6)),
                ('amount', models.FloatField(default=0)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterField(
            model_name='accountstatement',
            name='bookings',
            field=models.ManyToManyField(to='UWEFlix.Transaction'),
        ),
    ]
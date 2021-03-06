# Generated by Django 3.0.6 on 2020-07-18 04:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0009_doctors_hospital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctors',
            name='profession',
            field=models.CharField(choices=[('Neurologist', 'Neurologist'), ('Gynecologist', 'Gynecologist'), ('Dentist', 'Dentist')], max_length=75),
        ),
        migrations.CreateModel(
            name='doctor_review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('review_star', models.IntegerField()),
                ('review_msg', models.TextField()),
                ('date', models.DateField(default='2020-07-17')),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.doctors')),
            ],
        ),
    ]

# Generated by Django 3.0.6 on 2020-07-18 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0010_auto_20200717_2110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor_review',
            old_name='author_id',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='doctor_review',
            old_name='doctor_id',
            new_name='doctor',
        ),
        migrations.AlterField(
            model_name='doctor_review',
            name='date',
            field=models.DateField(default='2020-07-18'),
        ),
    ]

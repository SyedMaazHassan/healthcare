# Generated by Django 3.0.8 on 2020-07-13 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_auto_20200713_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctors',
            name='hospital',
            field=models.CharField(default='Liquiat National', max_length=75),
            preserve_default=False,
        ),
    ]
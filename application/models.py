from django.db import models
import datetime
from django.contrib.auth.models import User, auth
# Create your models here.


class department(models.Model):
    name = models.CharField(max_length=75, unique=True)
    related_profession_name = models.CharField(max_length=75)
    department_image = models.ImageField(upload_to='department_pics')
    short_description = models.CharField(max_length=75)

    def __str__(self):
        return self.name





class doctors(models.Model):
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    image = models.ImageField(upload_to='doctors_pic')
    email = models.CharField(max_length=75)
    city = models.CharField(max_length=75)
    password = models.CharField(max_length=20)

    # PROFESSION_CHOICES = (
    #     ("Neurologist", "Neurologist"),
    #     ("Gynecologist", "Gynecologist"),
    #     ("Physiologist", "Physiologist"),
    #     ("Orthopedic", "Orthopedic")
    # )

    temp_list = []
    
    all_depts = department.objects.all()

    for i in all_depts:
        temp_val = [i.related_profession_name, i.related_profession_name]
        temp_list.append(tuple(temp_val))
        print(temp_val)


    PROFESSION_CHOICES = tuple(temp_list)


    profession = models.CharField(choices = PROFESSION_CHOICES, max_length=75)
    hospital = models.CharField(max_length=75)

    
    def __str__(self):
        return self.first_name+"  -  "+self.email

    def save(self, *args, **kwargs):
        if not self.pk:
            new_doctor = User.objects.create_user(username=self.email, first_name=self.first_name, password=self.password, last_name=self.last_name)
            new_doctor.save()
        super(doctors, self).save(*args, **kwargs)


class appointment(models.Model):
    sender_patient = models.ForeignKey(User, on_delete=models.CASCADE)
    to_doctor = models.ForeignKey(doctors, on_delete=models.CASCADE)
    depart = models.CharField(max_length=50)
    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)
    status = models.IntegerField(default=0)

    # -1 = waiting for response
    #  0 = rejected
    #  1 = accepted
    #  2 = completed

class fakes(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    is_fake = models.BooleanField(default=True)
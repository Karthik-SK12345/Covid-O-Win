from django.db import models
from multiselectfield import MultiSelectField
# Create your models here.

class Patient(models.Model):
    name = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=15)
    patient_relative_name = models.CharField(max_length=50, null=True)
    patient_relative_contact = models.CharField(max_length=15, null=True)
    address = models.TextField()
    SYMPTOMS = (
        ('Fever', 'Fever'),
        ('Dry cough', 'Dry cough'),
        ('Tiredness', 'Tiredness'),
        ('Aches and pains', 'Aches and pains'),
        ('Sore throat', 'Sore throat'),
        ('Diarrhoea', 'Diarrhoea'),
        ('Loss of taste or smell', 'Loss of taste or smell'),
        ('Difficulty in breathing or shortness of breath', 'Difficulty in breathing or shortness of breath'),
        ('Chest pain or pressure', 'Chest pain or pressure'),
        ('Loss of speech or movement', 'Loss of speech or movement'),
    )

    symptoms = MultiSelectField(choices=SYMPTOMS, null=True)
    prior_ailments = models.TextField()
    bed_num = models.ForeignKey("Bed", on_delete=models.CASCADE)
    dob = models.DateField(null=True)
    doctor = models.ForeignKey("Doctor", on_delete=models.CASCADE, null=True)
    doctors_notes = models.TextField(null=True, blank=True)
    doctors_visiting_time = models.CharField(null=True, max_length=50, blank=True)
    status = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
        
class Bed(models.Model):
    bed_number = models.CharField(max_length=50)
    occupied = models.BooleanField()
    def __str__(self):
        return self.bed_number


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

import datetime
# Create your models here.
class Invoice(models.Model):
    customer = models.CharField(max_length=100)
    customer_email = models.EmailField(null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)
    date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    message = models.TextField(default= "this is a default message.")
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.customer)
    
    def get_status(self):
        return self.status

    # def save(self, *args, **kwargs):
        # if not self.id:             
        #     self.due_date = datetime.datetime.now()+ datetime.timedelta(days=15)
        # return super(Invoice, self).save(*args, **kwargs)

class LineItem(models.Model):
    customer = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    service = models.TextField()
    description = models.TextField()
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=9, decimal_places=2)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.customer)
   



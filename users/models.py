from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _
import random
from django.conf import settings
from django.urls import reverse

# Create your models here.

"""Generate account details"""
class Account(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    account_number = models.IntegerField()
    routine_number = models.IntegerField(default=4253674, editable=False)

    def __str__(self):
        return f"{self.user} account number is {self.account_number}"

    def save(self,*args, **kwargs):
        self.account_number = random.randint(1000001, 100000000)
        super().save(*args, **kwargs)

"""Model for message"""
class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    message = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    # read = models.BooleanField(default=False)
    read = models.CharField(max_length=30, default="No")

    class Meta:
        ordering = ['-date',]


    def __str__(self):
        return f"{self.user.username}: {self.message[:10]}"

    def get_absolute_url(self):
        return reverse("message_detail", kwargs={"pk":self.id})

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to ="profile", default="default-image.jpg")

    def __repr__(self):
        return f"{self.user} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        """ save images in a default size when uploaded"""
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


"""
For transactions
"""
class Typeof(models.TextChoices):
    send = "Transfered-Out", _("Transfered-Out")
    receive = "Received", _("Received")

class Progress(models.TextChoices):
    receive = "Processing", _("Processing")
    send = "Confirmed", _("Confirmed")

class Transaction(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    type_of = models.CharField(choices=Typeof.choices, max_length=70, default="Transfered-Out")
    bank_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    progress = models.CharField(choices=Progress.choices, max_length=70,default='Processing')
    date = models.DateField(auto_now_add=True)
    swift_code = models.CharField(default='ex: 4563h738738', max_length=15)
    account_number = models.IntegerField()
    routine_number = models.IntegerField()

    def __str__(self):
        return f"{self.user} transaction for date {self.date}"

    # def get_absolute_url(self):
    #         return reverse("local_transfer", kwargs={"pk":self.id})

class Payment(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    bank_name = models.CharField(max_length=25)
    account_number = models.IntegerField()
    routine_number = models.IntegerField()
    amount = MoneyField(default_currency="USD", default=0,max_digits=12)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
            return f"{self.user} transfer made for {self.amount} on {self.date}"


class Payment_Wire(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    bank_name = models.CharField(max_length=25)
    account_number = models.IntegerField()
    routine_number = models.IntegerField()
    swift_code = models.IntegerField()
    amount = MoneyField(default_currency="USD", default=0, max_digits=12)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
            return f"{self.user} wire transfer made for {self.amount} on {self.date}"



class Balance(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    balance = MoneyField(max_digits=14, default_currency='USD')

    def __str__(self):
        return f"{self.user} balance"


class Charge(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    bill = MoneyField(max_digits=14, default_currency='USD')

    def __str__(self):
        return f"{self.user} charges"
        


# class Country(models.TextChoices):
#     us = "Us", _("United States")
#     ch = "Ch", _("China")
    
class Setting(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    address = models.CharField(max_length=100)
    country = models.CharField( max_length=100)
    state = models.CharField(max_length=30)
    dob = models.DateTimeField()
    id_card = models.ImageField(upload_to="id_cards")

    def __str__(self):
        return f"{self.user} settings"

class identification(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    image = models.FileField()
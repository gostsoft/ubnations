from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from  .models import Balance, Charge, Profile, Message, Account
from djmoney.money import Money

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Charge.objects.create(user=instance,bill=Money(57, 'USD') ).save()
        Balance.objects.create(user=instance,balance=Money(0, 'USD')).save()
        Message.objects.create(user=instance, message ='Thanks for signing up with United Banking' ).save()
        Message.objects.create(user=instance, message ='Start making transactions' ).save()
        Message.objects.create(user=instance, message ='You are to make a payment, kindly check your dashboard' ).save()
        Account.objects.create(user=instance).save()

        
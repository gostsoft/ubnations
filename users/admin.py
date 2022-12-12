from django.contrib import admin

# Register your models here.
from .models import Transaction, Balance, Charge, Profile, Message, Payment,Account, Setting

# Register your models here.
admin.site.register([Transaction, Balance, Profile, Charge,Message,Payment,Account, Setting
])
from django.shortcuts import render, redirect
from users.forms import Payment_form, Reg_user, Dp, Prof, Set, Wire_Payment_form
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from .models import Message, Balance
from .models import Transaction, Setting
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from djmoney.money import Money


def error404(request, *args, **kwargs):
   
    return render(request=request, template_name="404.html")

# Create your views here.++++

def register(req):
    if req.method == "POST":
        form = Reg_user(req.POST)
        if form.is_valid():
            name = form.cleaned_data["first_name"]     
            form.save()       
            messages.success(req, f"You hahve successfully created an account {name}")
            print("signed up")
            print(req.POST)
            return redirect("login")
    form = Reg_user()
    return render(req, "sign-up.html", {'form':form}) 
   


@login_required
def order(req):
    print(req.user.balance.balance)  
    if str(req.user.balance.balance) == '$0.00':
        string = {'message': 'Sorry you will need to make a deposit'}
        return render(req, 'dashboard/failure.html', string)
    string = {'message': 'Sorry you will need to make some bills payment before you can withdraw'}
    return render(req, 'dashboard/failure.html', string)

"""Local transfer"""


def amountCheck(form, user):
    balance = user.balance.balance.amount
    withdraw = form.instance.amount.amount
    """checking if the withdrawal balance is greater than the balance"""

    if(withdraw <= balance):
        balance = balance - withdraw
        # Balance.object.update_or_create(user, balance=Money(balance, 'USD')).save()

        obj = Balance.objects.get(id=user.id)
        obj.balance = balance
        obj.save()
        print(balance)
        return True
    return False


class TransactionView(CreateView):
    model = Transaction
    exclude = ['date', 'progress', 'type_of', 'swift_code']
    form_class = Payment_form
    template_name="dashboard/local.html"
    success_url= reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user # setting the form user instance to the signed in user
        if(amountCheck(form, form.instance.user)):
            return super().form_valid(form)
        return HttpResponse("Sorry your balance is too low")
                 

    """The wire transfer view"""

class WireView(CreateView):
    model = Transaction
    exclude = ['date', 'progress', 'type_of',]
    form_class = Wire_Payment_form
    template_name="dashboard/wire.html"
    success_url= reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user # setting the form user instance to the signed in user
        if(amountCheck(form, form.instance.user)):
            return super().form_valid(form)
        return HttpResponse("Sorry your balance is too low")
        

    

@login_required
def activate(req):
    print(req.user.balance.balance)  
    if(req.user.balance.balance.amount == 0):
        string = {'message': 'Sorry you currently cant order a card, make a deposit'}
        return render(req, 'dashboard/failure.html', string)
        
    return render(req, 'dashboard/activate-card.html')


"""The profile dashboard"""
@login_required
def profile(req):
    user = req.user
    if req.method == "POST":
        dp = Dp(req.POST, req.FILES, instance=user.profile)
        user_prof = Set(req.POST, instance=user)
        if dp.is_valid() and user_prof.is_valid():
            user_prof.save()
            dp.save()
            context = {
                'message1':'Success',
                'message2': 'You have successfully updated your profile'
            }
            return render(req, 'dashboard/success.html', context)

    bal = {
     "profile_pic": user.profile.image,
     "udp": Dp(),
     'user_prof' :Set(instance=user)}
    return render(req, "dashboard/profile.html", bal)


@login_required
def transaction(req):
    user = req.user
    bal = {
     "all_transaction": user.transaction_set.all()}

    return render(req,"dashboard/transactions.html",bal)

class MessageView(DetailView):
    model = Message
    template_name= 'dashboard/message-details.html'

@login_required
def verify(req):
    user = req.user
    if req.method == "POST":
        # details = Setting.Objects.get(user_id=user.id)
        verify = Prof(req.POST, req.FILES)
        verify['user'] = user
        if verify.is_valid():
            verify.save()
            print("gone")
            context = {
                'message1':'Success: We will get back to you',
                'message2': 'You have successfully submitted your details for verification'
            }
            return render(req, 'dashboard/success.html', context)

    bal = {
     
     "verify": Prof(),
     'user_prof' :Set(instance=user)}
    return render(req, "dashboard/verify.html", bal)
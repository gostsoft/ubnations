"""secure_assets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
import users.views as vs 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='United Bank of Nations.html'), name="home"),#edied
     path('terms/', TemplateView.as_view(template_name='Terms and Conditions - United Bank of Nations.html'), name="tnc"),#edited
    path('login', LoginView.as_view(template_name='login.html'), name="login"),#edited
    path('logout', LogoutView.as_view(template_name='logout.html'), name="logout"),#edited
    path('open-account/', vs.register, name="register"),#edited, listed    
    path('contact/', TemplateView.as_view(template_name='Contact - United Bank of Nations.html'), name="contact"),# just details
    path('about/', TemplateView.as_view(template_name='About - United Bank of Nations.html'), name="about"),#edited
    #authenticated paths

    path('account-home/', login_required(TemplateView.as_view(template_name='dashboard/index.html')), name="dashboard"),#edited
    path('message/<int:pk>/', login_required(vs.MessageView.as_view()), name='message_detail'),

    path('localTransfer/',login_required(vs.TransactionView.as_view()), name ="local_transfer"),
    path('wireTransfer/', login_required(vs.WireView.as_view()), name="wire_transfer"),
    path('activate-card/', vs.activate, name="activate"),
    path('order-card/', vs.order, name="order"),#done
    path('transfer/', login_required(TemplateView.as_view(template_name='dashboard/transfer.html')), name="transfer"),#edited
    path('success/', login_required(TemplateView.as_view(template_name='dashboard/success.html')), name="success"),#edited
    path('vectorMap/', login_required(TemplateView.as_view(template_name='dashboard/vector.html')), name="vector"),#edited
    path('map/', login_required(TemplateView.as_view(template_name='dashboard/google.html')), name="google"),#edited
    path('transaction/',vs.transaction, name="transaction"),
    path('failure/', login_required(TemplateView.as_view(template_name='dashboard/failure.html')), name="failure"),#edited
    path('profile/', vs.profile, name="profile"),
    path('account-verification/', vs.verify, name="verify"),
]
if settings.DEBUG == True:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
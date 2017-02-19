"""baize URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from apps.accounts import accounts_controller, invite_code_controller

urlpatterns = [
    url(r'^$', accounts_controller.LoginView.as_view(), name="login"),
    url(r'^login$', accounts_controller.LoginView.as_view(), name="login"),

    # Invite code router begin.
    url(r'^admin/api/make_ic$', invite_code_controller.MakeInviteCodeView.as_view(), name="make_invite_code")
    # Invite code router end.
]

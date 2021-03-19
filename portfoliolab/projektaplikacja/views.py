from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from projektaplikacja.forms import UserAddForm, LoginForm
from projektaplikacja.models import Donation, Institution, Category, DonationCategories


class LandingPage(View):

    def get(self, request):
        worki = Donation.objects.all().aggregate(Sum('quantity'))
        suma_workow = worki['quantity__sum']
        wsparteorganizacje = Institution.objects.all().aggregate(Count('id'))
        wsparteorganizacjeliczba = wsparteorganizacje['id__count']
        fundacje = Institution.objects.filter(type=1)
        organizacjepozarzadowe = Institution.objects.filter(type=2)
        zbiorkalokalna = Institution.objects.filter(type=3)

        return render(request, 'index.html', {'zbiorkalokalna':zbiorkalokalna,
                                              'organizacjepozarzadowe':organizacjepozarzadowe,
                                              'suma_workow': suma_workow, 'wsparteorganizacje': wsparteorganizacje,
                                              'fundacje':fundacje,'wsparteorganizacjeliczba': wsparteorganizacjeliczba})


class AddDonation(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('../login/#login')
        else:
            categories = Category.objects.all()
            institutions = Institution.objects.all()
            return render(request, 'form.html', {'categories': categories, 'institutions': institutions})


class Register(View):

    def get(self, request):
        form = UserAddForm()
        return render(request, "register.html", {'form': form})

    def post(self, request):
        form = UserAddForm(request.POST)
        if form.is_valid():
            User.objects.create_user(username=form.cleaned_data['email'],
                                     password=form.cleaned_data['password'],
                                     email=form.cleaned_data['email'],
                                     first_name=form.cleaned_data['first_name'],
                                     last_name=form.cleaned_data['last_name']
                                     )
            return redirect('/login/')
        else:
            return render(request, "register.html", {'form': form})


class Login(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if User.objects.filter(username=username):
                if user:
                    login(request, user)
                    return redirect('../')
                else:
                    return render(request, 'login.html', {'form': form})
            else:
                return redirect('../../register/')
        else:
            return render(request, 'login.html', {'form': form})


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('/')


def DonationCategoryToString(donation):
    categories = DonationCategories.objects.filter(donation=donation)
    categoryList = []
    for category in categories:
        categoryList.append(category.category.name)
    str1 = ", "
    return str1.join(categoryList)


class UserView(View):

    def get(self, request):
        donations = Donation.objects.filter(user=request.user)
        for donation in donations:
            donation.category = DonationCategoryToString(donation)
        return render(request, 'user.html', {"donations": donations})
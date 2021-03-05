from django.db.models import Sum, Count
from django.shortcuts import render

# Create your views here.
from django.views import View

from projektaplikacja.models import Donation, Institution, Category


class LandingPage(View):

    def get(self, request):
        worki = Donation.objects.all().aggregate(Sum('quantity'))
        suma_workow = worki

        wsparteorganizacje = Institution.objects.all().aggregate(Count('id'))

        fundacje = Institution.objects.filter(type=1)

        kategorie = Category.objects.all()

        organizacjepozarzadowe = Institution.objects.filter(type=2)

        zbiorkalokalna = Institution.objects.filter(type=3)

        return render(request, 'index.html', {'zbiorkalokalna':zbiorkalokalna, 'organizacjepozarzadowe':organizacjepozarzadowe, 'suma_workow': suma_workow, 'wsparteorganizacje': wsparteorganizacje,'fundacje':fundacje})


class AddDonation(View):

    def get(self, request):
        return render(request, 'form.html')


class Login(View):

    def get(self, request):
        return render(request, 'login.html')


class Register(View):

    def get(self, request):
        return render(request, 'register.html')
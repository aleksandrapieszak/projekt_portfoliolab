from django.contrib import admin

# Register your models here.
from projektaplikacja.models import Institution, Donation, Category

admin.site.register(Institution)
admin.site.register(Donation)
admin.site.register(Category)


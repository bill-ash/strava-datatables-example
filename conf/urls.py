from unicodedata import name
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('datatables.urls', namespace='datatables')),

]

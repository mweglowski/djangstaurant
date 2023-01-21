from django.urls import path
from . import views

urlpatterns = [
	path('', views.HomeView.as_view(), name="home"),
	path('inventory/', views.inventory, name="inventory")
]
from django.shortcuts import render

# Create your views here.
def home(request):
	return render(request, "home.html")

def inventory(request):
	return render(request, "inventory.html")
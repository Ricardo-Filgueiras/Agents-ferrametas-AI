from django.shortcuts import render


app = "interface"


def home(request):
    return render(request, 'index.html')   
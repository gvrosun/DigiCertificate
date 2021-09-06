from django.shortcuts import render
from . models import User


# Create your views here.
def index(request):
    user_data = User.objects.all()
    return render(request, 'user/index.html', {
        'user_data': user_data
    })

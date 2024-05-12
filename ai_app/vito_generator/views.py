from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def userLogin(request):
    return render(request, 'login.html')

def userSignup(request):
    return render(request, 'signup.html')

# def userLogout(request):
#     return render(request, 'logout.html')

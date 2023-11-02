from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    context = {'page':'Home'}
    return render(request, 'home/index.html', context)


@login_required(login_url='/login')
def recipies(request):

    if request.method == 'POST':
        data = request.POST

        recipie_image = request.FILES.get('recipie_image')
        recipie_name = data.get('recipie_name')
        recipie_description = data.get('recipie_description')
        
        Recipie.objects.create(
            recipie_image = recipie_image,
            recipie_name = recipie_name,
            recipie_description = recipie_description,
            )
        
        return redirect('/recipies')
        
        # print(recipie_name)
        # print(recipie_description)
        # print(recipie_image)

    queryset = Recipie.objects.all()
    if request.GET.get('search'):
        # print(request.GET.get('search'))  #for debugging and testing   
        # __icontains is like fuzzywuzzy it checks that the search term is in the variable(string)
        
        queryset = queryset.filter(recipie_name__icontains = request.GET.get('search'))



    context = {'page':'Recipies', 'recipies':queryset}

    return render(request, 'home/recipies.html', context)


def update_recipie(request,id):

    queryset = Recipie.objects.get(id=id)

    if request.method == 'POST':
        data = request.POST

        recipie_image = request.FILES.get('recipie_image')
        recipie_name = data.get('recipie_name')
        recipie_description = data.get('recipie_description')

        queryset.recipie_name = recipie_name
        queryset.recipie_description = recipie_description

        if recipie_image:
            queryset.recipie_image = recipie_image

        queryset.save()
        return redirect('/recipies')


    context = {'page':'Update Recipie', 'recipie':queryset}
    return render(request, 'home/update_recipie.html', context)



def delete_recipie(request, id):
    queryset = Recipie.objects.get(id=id)
    queryset.delete()
    return redirect('/recipies')


def about(request):
    context = {'page':'About'}
    return render(request,'home/about.html', context)


def contact(request):
    context = {'page':'Contact'}
    return render(request, 'home/contact.html', context)

# Authentication:

def login_page(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user =  User.objects.filter(username=username)
        if not user.exists():
            messages.error(request, 'Invalid Username')
            return redirect('/recipies')
        
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid Username or Password')

        else:
            login(request, user)
            return redirect('/recipies')
        
  

    context = {'page':'Login Page'}
    return render(request, 'home/login.html', context)
        
 

def logout_page(request):
    logout(request)
    return redirect('/login')

        


def register(request):
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user =  User.objects.filter(username=username)
        if user.exists():
            messages.error(request, 'Username already taken')
            return redirect('/register')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            # password = password   it save password as user gave without encryption 
        )

        user.set_password(password)  # it encrypt password 
        user.save()
        
        messages.info(request, 'Account created successfully')


        return redirect('/login')



    context = {'page':'Registration'}
    return render(request, 'home/register.html', context)
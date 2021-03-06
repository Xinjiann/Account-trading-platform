from ast import Or
from calendar import c
from curses.ascii import US
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from django.urls import reverse
from rango.models import Category, GameAccount, Order, UserProfile
from django.contrib.auth.models import User
from rango.forms import UserForm, UserProfileForm
import time
from django.contrib.auth.decorators import login_required




def show_category(request,category_name_slug):
    context_dict = {}
    try:
        category = 'fortnite'
        accounts = GameAccount.objects.filter(category=category)
        context_dict['accounts']=accounts
        context_dict['category']=category
        print (accounts)
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['accounts'] = None
    
    return render(request,'rango/category.html',context_dict)


def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    
    context_dict = {}

    context_dict['boldmessage'] = 'LOL, CS:GO, Overwatch, Warcraft and Fornite! '
    context_dict['categories'] = category_list
    return render(request, 'rango/index.html', context=context_dict)


def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,'rango/register.html',
                  context = {'user_form': user_form,'profile_form': profile_form,'registered': registered})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                rep = redirect(reverse('rango:index'))
                rep.set_cookie('name', username)
                return rep
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
        # The request is not a HTTP POST, so display the login form.
        # This scenario would most likely be a HTTP GET
    else:
    # No context variables to pass to the template system, hence the
    # blank dictionary object...
        return render(request, 'rango/login.html')


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('rango:index'))



def account_detail(request, account_name):
    # GameAccount.objects.all()    
    account_list = GameAccount.objects.filter(accountName=account_name)
    # account_list = GameAccount.objects.get(accountName=account_name)
    context_dict = {}
    context_dict['accountList'] = account_list
    
    return render(request, 'rango/accountDetail.html', context=context_dict)

def myaccount(request):
    name = request.COOKIES.get('name')
    user = User.objects.get(username=name)
    user2 = UserProfile.objects.filter(user=user)
    context_dict = {}
    context_dict['userprofile'] = user2
    return render(request, 'rango/myaccount.html', context=context_dict)

def myorder(request):
    user = request.COOKIES.get('name')
    orders = Order.objects.filter(buyer=user)

    context_dict = {}
    context_dict['orders'] = orders
    return render(request, 'rango/myorder.html', context=context_dict)

def buy(request, name):

    username = request.COOKIES.get('name')
    account = GameAccount.objects.get(accountName=name)

    user = User.objects.get(username=username)
    user1 = UserProfile.objects.get(user=user)
    if (user1.balance < account.price) :
        return HttpResponse("Balance not enough!")
    
    account.status = 'sold'
    user1.balance -= account.price
    account.save()
    user1.save()
    

    order = Order(accountName=name, date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), buyer=request.COOKIES.get('name'), password=account.password)
    order.save()
    return account_detail(request, name)

def popup(request):
    if request.method == 'POST':
        charge = request.POST.get('charge')
        name = request.COOKIES.get('name')
        user = User.objects.get(username=name)
        user2 = UserProfile.objects.get(user=user)
        user2.balance += int(charge)
        user2.save()
    return myaccount(request)

def accountList(request,name):
    list = GameAccount.objects.filter(category=name)

    context_dict = {}
    context_dict['accounts'] = list
    return render(request, 'rango/accountList.html', context=context_dict)


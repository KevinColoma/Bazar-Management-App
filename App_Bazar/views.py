from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from App_Bazar.forms import CategoryForm, BazarForm, CommentForm, PendingBazarForm, QueryForm
from django.contrib import messages 
from App_Bazar.models import Bazar, Category, PendingBazar
from App_Login.models import User
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import TruncDate
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Create your views here.
@login_required
def home(request):
    user = request.user
    bazar = Bazar.objects.all()
    total_cost = sum(item.total_cost() for item in bazar)
 
    form = BazarForm()
    if request.method == 'POST':
        form = BazarForm(data=request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.author = user
            user_form.save()
            messages.success(request, 'New bazaar item added')
            return HttpResponseRedirect(reverse('App_Bazar:home'))
    return render(request, 'App_Bazar/home.html', context={'form':form, 'total_cost':total_cost})

@login_required
def add_category(request):
   
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.user = request.user
            user_form.save()
            messages.success(request, 'New category added')
            return HttpResponseRedirect(reverse('App_Bazar:home'))


    return render(request, 'App_Bazar/add_category.html', context={'form':form})

@login_required
def history(request):
    has_categories = Category.objects.filter(user=request.user).exists()
    return render(request, 'App_Bazar/user_history.html', context={ 'has_categories':has_categories })

@login_required
def edit_bazar(request, pk):
    bazar = Bazar.objects.get(author=request.user, pk=pk)
    form = BazarForm(instance = bazar)

    if request.method == 'POST':
        form = BazarForm(data=request.POST, instance=bazar)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bazar updated successfully :D')
            return HttpResponseRedirect(reverse('App_Bazar:history'))
    return render(request, 'App_Bazar/edit_bazar.html', context={'form':form})

@login_required
def delete_bazar(request, pk):
    bazar = Bazar.objects.get(author=request.user, pk=pk)
    bazar.delete()
    messages.warning(request, 'Bazar deleted!')
    return HttpResponseRedirect(reverse('App_Bazar:history'))

@login_required
def others_bazar(request, pk):
    bazar_user = User.objects.get(pk=pk)
    bazars = Bazar.objects.filter(author=bazar_user)
    has_categories = Category.objects.filter(user=bazar_user).exists()
    categories = Category.objects.filter(user=bazar_user)
    return render(request, 'App_Bazar/others_bazar.html', context={'bazars':bazars, 'bazar_user':bazar_user, 'has_categories':has_categories, 'categories':categories})


@login_required
def categories(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'App_Bazar/user_categories.html', context={'categories':categories})

@login_required
def update_category(request, pk):
    category = Category.objects.get(pk=pk)
    form = CategoryForm(instance=category)

    if request.method == 'POST':
        form = CategoryForm(data=request.POST, instance=category)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.user = request.user
            user_form.save()
            messages.success(request, 'Category updated successfully')
            return HttpResponseRedirect(reverse('App_Bazar:history'))
    return render(request, 'App_Bazar/update_category.html', context={'form':form})

@login_required
def delete_category(request, pk):
    category = Category.objects.get(pk=pk)

    if Category.objects.filter(user=request.user, pk=category.pk).exists():
        category.delete()
        messages.warning(request, 'Category deleted!')
        return HttpResponseRedirect(reverse('App_Bazar:history'))
    

@login_required
def pending_bazars(request):
    logged_in_user = request.user
    pending_bazars = PendingBazar.objects.all()

    return render(request, 'App_Bazar/pending_bazars.html', context={'pending_bazars':pending_bazars, 'logged_in_user':logged_in_user})

@login_required
def update_pending_bazar(request, pk):
    pending_bazar = PendingBazar.objects.get(author=request.user, pk=pk)
    form = PendingBazarForm(instance=pending_bazar)
    if request.method == 'POST':
        form = PendingBazarForm(data=request.POST, instance=pending_bazar)
        if form.is_valid():
            form.save()
            messages.info(request, 'Pending bazar updated successfully')
            return HttpResponseRedirect(reverse('App_Bazar:pending_bazars'))
    return render(request, 'App_Bazar/update_pending_bazar.html', context={'form':form})

@login_required
def complete_pending_bazar(request, pk):
    pending_bazar = PendingBazar.objects.get( pk=pk)
    pending_bazar.delete()
    messages.success(request, 'Bazar done :D')
    return HttpResponseRedirect(reverse('App_Bazar:pending_bazars'))

@login_required
def add_pending_bazar(request):
    bazar_author = request.user
    form = PendingBazarForm()
    if request.method == 'POST':
        form = PendingBazarForm(data=request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.author = bazar_author
            user_form.save()
            messages.success(request, 'New todo added')
            return HttpResponseRedirect(reverse('App_Bazar:pending_bazars'))
    return render(request, 'App_Bazar/add_pending_bazar.html', context={'form':form})
    
@login_required
def bazar_history(request):
    # Use TruncDate to truncate datetime to date
    bazar_dates = Bazar.objects.annotate(date_only=TruncDate('publish_date')).values_list('date_only', flat=True).distinct()
    return render(request, 'App_Bazar/all_bazar_dates.html', context={'bazar_dates': bazar_dates})

@login_required
def sorted_bazar(request, date):
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    bazars = Bazar.objects.annotate(date_only=TruncDate('publish_date')).filter(date_only=date_obj)
    print(bazars)
    return render(request, 'App_Bazar/individual_bazar.html', context={'bazars':bazars})



@login_required
def ask_ai(request):
    genai.configure(api_key=os.environ["API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    answer = ""
    form = QueryForm()

    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            response = model.generate_content(question.query)
            answer = response.text


    return render(request, "App_Bazar/query.html", context={'form': form, 'answer': answer})
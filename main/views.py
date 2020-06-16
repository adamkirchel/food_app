from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import NewUserForm,LarderForm,TimetableForm,LoginForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .models import larderItems, recipes, Event
from .python.main.recipe_bot import find_recipe, find_recipe_types
from .python.main.shopping_basket import shopping_basket
from .utils import Calendar
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import datetime



def single_slug(request, single_slug):
    
    recipe_list = [t.title for t in recipes.objects.all()]
    print(recipe_list[1])
    print(single_slug)
    
    if single_slug in recipe_list:
    
        recipe_object = recipes.objects.filter(title = single_slug)
        recipe_object = recipe_object.last()
        
        ingredients_list = eval(recipe_object.ingredients)
        ingredients = []
        
        for key in ingredients_list:
        
            ingredients.append(key)
            sub_list = ingredients_list[key]
            ingredients.extend(sub_list)
            
        print(Event.objects.values('title'))
        
        if request.method == "POST":
            print('a')
            form = TimetableForm(request.POST)

            if form.is_valid():
         
                fs = form.save(commit=False)
                fs.title = single_slug
                
                fs.ingredients = ingredients
                
                print(fs.title)
                
                fs.user = request.user.username
                
                fs.save()
                
                
                
                form = TimetableForm()
                
                return render(request,
                          "main/recipe_page.html",
                          {"recipe_object":recipe_object,
                           "ingredients":ingredients,
                           "form":form})

        #full_ingredients = list(ingredients_list.values())[0]
        form = TimetableForm()
        
        return render(request,
                      "main/recipe_page.html",
                      {"recipe_object":recipe_object,
                       "ingredients":ingredients,
                       "form":form})
        
    return HttpResponse(f"{single_slug} does not correspond to anything.")
                  
def account(request):

    return render(request=request,
                  template_name="main/account.html")
                  
def cabinet(request):
    
    if request.method == "GET":
        
        
        item = request.GET.get('remove')
        print(item)
        larderItems.objects.filter(item=item).delete()
        
        
        
    if request.method == "POST" and 'Add' in request.POST:
        
        form = LarderForm(request.POST)
        print(form)
        if form.is_valid():
        
            fs = form.save(commit=False)
            fs.user = request.user.username
            
            fs.save()
            
            username = fs.user
            
            larder_objects = larderItems.objects.filter(
                user = username)
                
            larder_categories = ['all','fresh','grains','baking','canned','drinks','snacks','other']
                
            form = LarderForm()
            
            larder_dict = list(larder_objects.values('item'))
            larder_list = [d['item'] for d in larder_dict]
            
            recipe_list = find_recipe(' '.join(larder_list))

                
            return render(request=request,
                          template_name="main/cabinet.html",
                          context={'form':form,
                                   'larder_objects':larder_objects,
                                   'recipes':recipe_list,
                                   'categories':larder_categories})
                
    
    
    
    form = LarderForm()
    
    username = request.user.username
    
    larder_objects = larderItems.objects.filter(
                user = username)
                
    larder_dict = list(larder_objects.values('item'))
    larder_list = [d['item'] for d in larder_dict]
    
    recipe_list = find_recipe(' '.join(larder_list))

    return render(request=request,
                  template_name="main/cabinet.html",
                  context={'form':form,
                           'larder_objects':larder_objects,
                           'recipes':recipe_list})
def kitchen(request):

    username = request.user.username
    
    larder_objects = larderItems.objects.filter(
                user = username)
                
    larder_dict = list(larder_objects.values('item'))
    larder_list = [d['item'] for d in larder_dict]

    #recipe_list,image_list = find_recipe(' '.join(larder_list))
    
    cake_list = find_recipe_types('cake')
    chicken_list = find_recipe_types('chicken')
    salad_list = find_recipe_types('salad')
    italian_list = find_recipe_types('Spaghetti lasagne parmigiana rigatoni pizza penne carbonara pasta fettucine macaroni ravioli parma parmigiano gorgonzola gnocchi bolognese italian pancetta')
    print(cake_list)
    
    return render(request=request,
                  template_name="main/kitchen.html",
                  context={'chicken_list':chicken_list,                          
                           'cake_list':cake_list,                          
                           'salad_list':salad_list,
                           'italian_list':italian_list})
                 
                  
def timetable(request):

    return render(request=request,
                  template_name="main/timetable.html")       

def login_request(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password")
        else:
                messages.error(request, "Invalid username or password")
        
    form = LoginForm()
    return render(request,
                  "main/login.html",
                  context={"form":form})
                  
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")
                  
def register(request):

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            return redirect("main:homepage")
            
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")

            return render(request=request,
                          template_name="main/register.html",
                          context={"form":form})
    
    form = NewUserForm()
    print(form)
    return render(request=request,
                          template_name="main/register.html",
                          context={"form":form})
                          
# Create your views here.
def homepage(request):

    return render(request=request, 
                  template_name="main/homepage.html")
                  
                  
def mealplan(request):

    if request.method == "GET":
        
        item = request.GET.get('remove')
        print(item)
        Event.objects.filter(title=item).delete()

    if request.method == "POST" and 'previous' in request.POST:
    
        d = get_date(self.request.GET.get('month', None))
        previous_month = prev_month(d)
        d = get_date(previous_month)
        
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        return render(request=request,
                      template_name="main/mealplan.html",
                      context={"calendar":html_cal})  

    def get_date(req_day):
        if req_day:
            year, month = (int(x) for x in req_day.split('-'))
            return date(year, month, day=1)
        return datetime.today()

    # use today's date for the calendar
    d = get_date(request.GET.get('day', None))

    # Instantiate our calendar class with today's year and date
    cal = Calendar(d.year, d.month)

    # Call the formatmonth method, which returns our calendar as a table
    html_cal = cal.formatmonth(withyear=True)
    #context['calendar'] = mark_safe(html_cal)
    return render(request=request,
                  template_name="main/mealplan.html",
                  context={"calendar":html_cal})  
                  
def shopping_list(request):

    shopping_list = shopping_basket(larderItems,Event)
    
    return render(request,
                  "main/shopping_cart.html",
                  {"shopping_list":shopping_list})
                

class CalendarView(generic.ListView):
    ...
    def get_context_data(self, **kwargs):
        ...
        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
    
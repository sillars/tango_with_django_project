from django.shortcuts import render

from django.http import HttpResponse

# Import the Category and Page models
from rango.models import Category
from rango.models import Page

from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse

from django.contrib.auth import authenticate, login

def index(request):
	# Query the db for a list of all categories currently stored.
	# Order the categories by the number of likes in descending order.
	# Retrieve only the top 5 (if less than 5 then retreive all)
	# Place the list in our context_dict that will be passed to the template engine
	category_list = Category.objects.order_by('-likes')[:5]
	pages_list = Page.objects.order_by('-views')[:5]

	context_dict = {}
	context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
	context_dict['categories'] = category_list
	context_dict['pages'] = pages_list
	# Render the response and return
	return render(request, 'rango/index.html', context=context_dict)

def about(request):
	about_context_dict = {'boldmessage': 'This tutorial has been put together by Mairi Sillars'}
	return render(request, 'rango/about.html', context=about_context_dict)
	
# Category pages
def show_category(request, category_name_slug):
	context_dict={}
	
	try:
		# Try to find a category with the name slug
		category = Category.objects.get(slug=category_name_slug)
		
		# Retrieve all of the associated pages
		pages = Page.objects.filter(category=category)
		
		# Add the results list and the category object 
		# from the database to the template
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		context_dict['category'] = None
		context_dict['pages'] = None
	
	return render(request, 'rango/category.html', context=context_dict)
	
# Display the category form and handle the posting of form data
def add_category(request):
	form = CategoryForm()
	
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		
		if form.is_valid():
			# Save the new category to the db
			form.save(commit=True)
			return redirect('/rango/')
		else:
			# The form contained errors
			print(form.errors)
			
	return render(request, 'rango/add_category.html', {'form': form})
	
def add_page(request, category_name_slug):
	try:
		category = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category = None

	# You cannot add a page to a Category that does not exist
	if category is None:
		return redirect('/rango/')

	form = PageForm()
	
	if request.method == 'POST':
		form = PageForm(request.POST)
		
		if form.is_valid():
			if category:
				# Save the new page to the db
				page = form.save(commit=False)
				page.category = category
				page.views = 0
				page.save()
				
				return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
		else:
			# The form contained errors
			print(form.errors)
			
	context_dict = {'form': form, 'category': category}		
	return render(request, 'rango/add_page.html', context=context_dict)
	
def register(request):
	# To tell the template whether the registration was successfull
	registered = False
	
	# If it's a HTTP POST, we're interested in processing form data
	if request.method == 'POST':
		# Attempt to grab info from the raw form info
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			
			# Hash the password and update user object
			user.set_password(user.password)
			user.save()
			
			# Since setting attributes, delay saving the model with
			# commit = False
			profile = profile_form.save(commit=False)
			profile.user = user
			
			# Is there profile picture provided?
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
				
			profile.save()
			
			registered = True
			
		else:
			# Invalid form(s) 
			print(user_form.errors, profile_form.errors)
	else:
		# Not a HTTP POST, render form using two ModelForm instances
		user_form = UserForm()
		profile_form = UserProfileForm()
		
	return render(request, 'rango/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
	
def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(username=username, password=password)
		
		if user:
			if user.is_active:
				login(request, user)
				return redirect(reverse('rango:index'))
			else:
				return HttpResponse("Your Rango account is disabled")
				
		else:
			print(f'Invalid login details: {username}, {password}')
			return HttpResponse("Invalid login details supplied.")
				
	else:
		return render(request, 'rango/login.html')
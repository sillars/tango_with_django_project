from django.shortcuts import render

from django.http import HttpResponse

# Import the Category and Page models
from rango.models import Category
from rango.models import Page

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
	

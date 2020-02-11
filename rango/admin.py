from django.contrib import admin
from rango.models import Category, Page

class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'url')

# Register your models here.
admin.site.register(Category)
admin.site.register(Page, PageAdmin)
#to add more classes, simply call admin.site.register()
#and make sure the model is imported at the top
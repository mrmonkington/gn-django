from django.contrib import admin
from .models import FieldValidatorExample

class FieldValidatorExampleAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(FieldValidatorExample, FieldValidatorExampleAdmin)

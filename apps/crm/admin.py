from django.contrib import admin
from apps.crm.models import *
# Register your models here.
@admin.register(items)
class itemsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'rate', 'unit_type'] 

@admin.register(itemCategory)
class itemCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    
class ProjectFileInline(admin.TabularInline):
    model = ProjectFile

@admin.register(crmProjects)
class crmProjectsAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'project_type', 'client', 'price']
    inlines = [ProjectFileInline]

@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ('project', 'upload_file')

    
@admin.register(crmTasks)
class crmTasksAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'start_date', 'deadline', 'status']
    
admin.site.register(Invoice)

admin.site.register(Payments)

admin.site.register(Expense)

admin.site.register(YearlyPaymentStatistics)

admin.site.register(InvoiceItem)
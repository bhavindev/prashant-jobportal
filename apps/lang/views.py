from django.shortcuts import render, redirect
from apps.lang.models import Languages
from apps.lang.forms import LanguageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.decorators import admin_role_required

# Admin Language
@login_required(login_url='signIn')
@admin_role_required
def adminLanguageHome(request):
    languages = Languages.objects.all()
    
    context = {
        'title' : 'Languages',
        'languages' : languages
    }
    return render(request, 'admin/front/main/locale/index.html', context)

@login_required(login_url='signIn')
@admin_role_required
def adminLanguageCreate(request):
    form = LanguageForm()
    if request.method == 'POST':
        form = LanguageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Language Created Successfully')
            return redirect('adminLanguageHome')
    context = {
        'title' : 'Create Language',
        'form' : form
    }
    return render(request, 'admin/front/main/locale/create.html', context)

@login_required(login_url='signIn')
@admin_role_required
def adminLanguageEdit(request, code):
    language = Languages.objects.get(code=code)
    form = LanguageForm(instance=language)
    
    if request.method == 'POST':
        form = LanguageForm(request.POST, request.FILES, instance=language)
        if form.is_valid():
            if not form.cleaned_data['is_default'] and not Languages.objects.exclude(code=code).filter(is_default=True).exists():
                messages.warning(request, 'Cannot unset default language. Please make another language default first.')
                return redirect('adminLanguageHome')
            form.save()
            messages.success(request, 'Language Updated Successfully')
            return redirect('adminLanguageHome')
        
    context = {
        'title': 'Edit Language',
        'form': form,
        'language': language
    }
    return render(request, 'admin/front/main/locale/edit.html', context)

@login_required(login_url='signIn')
@admin_role_required
def adminLanguageDelete(request, code):
    language = Languages.objects.get(code=code)
    language.delete()
    messages.warning(request, 'Language Deleted Successfully')
    return redirect('adminLanguageHome')
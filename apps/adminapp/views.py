from django.shortcuts import render, redirect, get_object_or_404
from apps.homepage.models import *
from apps.aboutpage.models import *
from apps.authapp.models import *
from apps.adminapp.forms import *
from apps.blog.models import *
from apps.servicepage.models import *
from apps.portfoliopage.models import *
from apps.pricingpage.models import *
from apps.crm.models import *
from apps.settings.models import *
from apps.legals.models import agreement
from apps.legals.forms import agreementStatusForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from core.decorators import admin_role_required, both_role_required
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from apps.analytics.utils import *
from apps.lang.models import Languages


# Admin HomePage
@login_required(login_url='signIn')
@both_role_required
def adminHome(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    # Revenue Expense
    total_revenue = Payments.objects.aggregate(total_revenue=Sum('payment_ammount'))
    total_revenue = total_revenue['total_revenue'] if total_revenue['total_revenue'] is not None else 0

    total_expense = Expense.objects.aggregate(total_expense=Sum('amount'))
    total_expense = total_expense['total_expense'] if total_expense['total_expense'] is not None else 0

    profit = total_revenue - total_expense
    
    # Invoices
    invoice = Invoice.objects.all()
    paid_count = Invoice.objects.filter(status='PAID').count()
    unpaid_count = Invoice.objects.filter(status='UNPAID').count()
    
    # Count tasks for each status
    tasks = crmTasks.objects.all()
    to_do_count = crmTasks.objects.filter(status='to_do').count()
    in_progress_count = crmTasks.objects.filter(status='in_progress').count()
    done_count = crmTasks.objects.filter(status='done').count()
    
    # Project
    project_count = crmProjects.objects.all().count()
    client_project = crmProjects.objects.filter(project_type='client_project').count()
    internal_project = crmProjects.objects.filter(project_type='internal_project').count()
    
    # Payments
    payments = Payments.objects.all().order_by('-payment_date')
    expenses = Expense.objects.all().order_by('-date_of_expense')
    
    service_sections = serviceSection.objects.filter(language__code=default_language_code)
    projects_sections = projectsSection.objects.filter(language__code=default_language_code)
    project_categories = projectCategory.objects.all()
    fun_fact_sections = funFactSection.objects.all()
    testimonials_sections = testimonialsSection.objects.filter(language__code=default_language_code)
    team_members = teamSection.objects.filter(language__code=default_language_code)
    clients = clientsSection.objects.filter(language__code=default_language_code)
    blog  = blogs.objects.filter(language__code=default_language_code)
    blog_categories = blogCategory.objects.all()
    contact_submissions = contact.objects.all()
    subscribers = Subscriber.objects.all()
    
    # Analytics Data
    analytics = analyticsData(request)
    
    # Delete blank invoices
    Invoice.delete_blank_invoices()
    
    context = {
        'title' : 'Dashboard',
        'services': service_sections,
        'projects': projects_sections,
        'project_categories': project_categories,
        'funfacts': fun_fact_sections,
        'testimonials': testimonials_sections,
        'teams': team_members,
        'clients': clients,
        'blog': blog,
        'blog_categories' : blog_categories,
        'contact_submissions' : contact_submissions,
        'subscribers' : subscribers,
        'payments' : payments,
        'expenses' : expenses,
        
        # Revenue Expense Chart
        'total_revenue': total_revenue,
        'total_expense': total_expense,
        'profit' : profit,
        
        # Invoice Chart
        'invoice': invoice,
        'paid_invoice' : paid_count,
        'unpaid_invoice' : unpaid_count,
        
        # Task Chart
        'tasks': tasks,
        'to_do' : to_do_count,
        'in_progress' : in_progress_count,
        'done' : done_count,
        
        # Project Chart
        'project_count' : project_count,
        'client_project' :  client_project,
        'internal_project' : internal_project,
        
        # Analytics
        'analytics' : analytics,
    }
    
    return render(request, 'admin/front/main/index.html', context)

# Admin Blog
@login_required(login_url='signIn')
@both_role_required
def adminBlogHome(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    blog  = blogs.objects.filter(language__code=default_language_code)
    
    language_code = request.GET.get('language')
    
    if language_code:
        blog = blogs.objects.filter(language__code=language_code)
    
    context = {
        'title' : 'Blogs',
        'blogs': blog,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,  
        'default_language_code': default_language_code,
    }
    
    return render(request, 'admin/front/main/blog/blogs.html', context)

@login_required(login_url='signIn')
@both_role_required
def adminBlogCreate(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    categories = blogCategory.objects.filter(language__code=default_language_code)
    
    language_code = request.GET.get('language')
    
    if language_code:
        categories = blogCategory.objects.filter(language__code=language_code)
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        category = request.POST.get('category')
        if form.is_valid():
            blog = form.save(commit=False)
            blog.category = blogCategory.objects.get(id=category)
            blog.language = Languages.objects.get(code=language_code)
            blog.save()
            messages.success(request, 'Blog created successfully!')
            return redirect(reverse('adminBlogHome') + f'?language={language_code}')
    else:
        form = BlogForm()
    
    context = {
        'title' : 'Create Blog',
        'form': form,
        'categories': categories,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,  
        'default_language_code': default_language_code,
    }
    
    return render(request, 'admin/front/main/blog/create.html', context)

@login_required(login_url='signIn')
@both_role_required
def adminBlogEdit(request, slug):
    blog = get_object_or_404(blogs, slug=slug)
    language_code = blog.language.code
    
    categories = blogCategory.objects.filter(language__code=language_code)
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        category = request.POST.get('category')
        if form.is_valid():
            blog = form.save(commit=False)
            blog.category = blogCategory.objects.get(id=category)
            blog.save()
            messages.success(request, 'Blog updated successfully!')
            return redirect(reverse('adminBlogHome') + f'?language={blog.language.code}')
    else:
        form = BlogForm(instance=blog)
    
    context = {
        'title' : 'Edit Blog',
        'form': form,
        'blog' : blog,
        'categories': categories,
    }
    
    return render(request, 'admin/front/main/blog/edit.html', context)

@login_required(login_url='signIn')
@both_role_required
def adminBlogDelete(request, slug):
    blog = get_object_or_404(blogs, slug=slug)
    blog.delete()
    messages.warning(request, 'Blog deleted!')
    return redirect('adminBlogHome')

# Admin Blog Category
@login_required(login_url='signIn')
@both_role_required
def adminBlogCategoryHome(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    categories = blogCategory.objects.filter(language__code=default_language_code)
    
    language_code = request.GET.get('language')
    
    if language_code:
        categories = blogCategory.objects.filter(language__code=language_code)
    
    context = {
        'title' : 'Blog Categories',
        'blog_categories': categories,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,  
        'default_language_code': default_language_code,
    }
    
    return render(request, 'admin/front/main/blog/partial/category/categories.html', context)

@login_required(login_url='signIn')
def adminBlogCategoryCreate(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language', default_language_code)
    
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST)
        if form.is_valid():
            blog_category = form.save(commit=False)
            blog_category.language = Languages.objects.get(code=language_code)
            blog_category.save()
            messages.success(request, 'Category created successfully!')
            return redirect(reverse('adminBlogCategoryHome') + f'?language={language_code}')
    else:
        form = BlogCategoryForm()
    
    context = {
        'title' : 'Create Blog Category',
        'form': form,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,  
        'default_language_code': default_language_code,
    }
    
    return render(request, 'admin/front/main/blog/partial/category/create.html', context)

@login_required(login_url='signIn')
@both_role_required
def adminBlogCategoryEdit(request, slug):
    blog_category = get_object_or_404(blogCategory, slug=slug)
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST, instance=blog_category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect(reverse('adminBlogCategoryHome') + f'?language={blog_category.language.code}')
    else:
        form = BlogCategoryForm(instance=blog_category)
    
    context = {
        'title' : 'Edit Blog Category',
        'form': form,
        'blog_category' : blog_category,
    }
    
    return render(request, 'admin/front/main/blog/partial/category/edit.html', context)

@login_required(login_url='signIn')
@both_role_required
def adminBlogCategoryDelete(request, slug):
    blog_category = get_object_or_404(blogCategory, slug=slug)
    blog_category.delete()
    messages.warning(request, 'Category deleted!')
    return redirect('adminBlogCategoryHome')

# Admin Services
@login_required(login_url='signIn')
@admin_role_required
def serviceHome(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    services = serviceSection.objects.filter(language__code=default_language_code)
    
    language_code = request.GET.get('language')
    
    if language_code:
        services = serviceSection.objects.filter(language__code=language_code)
    
    context = {
        'title' : 'Services',
        'services': services,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,
        'default_language_code': default_language_code,
    }
    
    return render(request, 'admin/front/main/service/services.html', context)

@login_required(login_url='signIn')
@admin_role_required
def createService(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language', default_language_code)
    
    if request.method == 'POST':
        form = serviceForm(request.POST, request.FILES)
        order = request.POST.get('order')
        if serviceSection.objects.filter(order=order).exists():
            messages.warning(request, f'Order {order} already exists in another service.')
            return redirect(reverse('createService') + f'?language={language_code}')
        if form.is_valid():
            service = form.save(commit=False)
            service.language = Languages.objects.get(code=language_code)
            service.save()
            messages.success(request, 'Service created successfully!')
            return redirect(reverse('services') + f'?language={language_code}')
    else:
        form = serviceForm()
    
    context = {
        'title' : 'Create Service',
        'form': form,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,  
        'default_language_code': default_language_code,
    }
    
    return render(request, 'admin/front/main/service/create.html', context)

@login_required(login_url='signIn')
@admin_role_required
def editService(request, slug):
        service = get_object_or_404(serviceSection, slug=slug)
        if request.method == 'POST':
            form = serviceForm(request.POST, request.FILES, instance=service)
            order = request.POST.get('order')
            if serviceSection.objects.filter(order=order).exclude(slug=slug).exists():
                messages.warning(request, f'Order {order} already exists in another service.')
                return redirect(reverse('editService', args=[slug]))
            if form.is_valid():
                form.save()
                messages.success(request, 'Service updated successfully!')
                return redirect(reverse('services') + f'?language={service.language.code}')
        else:
            form = serviceForm(instance=service)
        
        context = {
            'title' : 'Edit Service',
            'form': form,
            'service': service,
        }
        
        return render(request, 'admin/front/main/service/edit.html', context)

@login_required(login_url='signIn')
@admin_role_required
def deleteService(request, slug):
        service = get_object_or_404(serviceSection, slug=slug)
        service.delete()
        messages.warning(request, 'Service deleted!')
        return redirect('services')

# Admin Projects
@login_required(login_url='signIn')
@admin_role_required
def projectHome(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    projects = projectsSection.objects.filter(language__code=default_language_code)
    
    language_code = request.GET.get('language')
    
    if language_code:
        projects = projectsSection.objects.filter(language__code=language_code)
        
    context = {
        'title' : 'Projects',
        'projects': projects,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,  
        'default_language_code': default_language_code,
    }
    
    return render(request, 'admin/front/main/project/projects.html', context)

@login_required(login_url='signIn')
@admin_role_required
def createProject(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    categories = projectCategory.objects.filter(language__code=default_language_code)
    
    language_code = request.GET.get('language', default_language_code)
    
    if language_code:
        categories = projectCategory.objects.filter(language__code=language_code)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        category = request.POST.get('category')
        order = request.POST.get('order')
        if projectsSection.objects.filter(order=order).exists():
            messages.warning(request, f'Order {order} already exists in another project.')
            return redirect(reverse('createProject') + f'?language={language_code}')
        if form.is_valid():
            project = form.save(commit=False)
            project.category = projectCategory.objects.get(id=category)
            project.language = Languages.objects.get(code=language_code)
            project.save()
            messages.success(request, 'Project created successfully!')
            return redirect(reverse('projects') + f'?language={language_code}')
    else:
        form = ProjectForm()
    context = {
        'title': 'Create Project',
        'form': form,
        'categories': categories,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,  
        'default_language_code': default_language_code,
    }
    return render(request, 'admin/front/main/project/create.html', context)

@login_required(login_url='signIn')
@admin_role_required
def editProject(request, slug):
    project = get_object_or_404(projectsSection, slug=slug)
    
    language_code = project.language.code

    categories = projectCategory.objects.filter(language__code=language_code)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        category = request.POST.get('category')
        order = request.POST.get('order')
        if projectsSection.objects.filter(order=order).exclude(slug=slug).exists():
            messages.warning(request, f'Order {order} already exists in another project.')
            return redirect(reverse('editProject', args=[slug]))
        if form.is_valid():
            project = form.save(commit=False)
            project.category = projectCategory.objects.get(id=category)
            project.save()  # Make sure to save the changes
            messages.success(request, 'Project updated successfully!')
            return redirect(reverse('projects') + f'?language={project.language.code}')
        else:
            print(form.errors)  # Print form errors if the form is invalid
            messages.error(request, 'There was an error updating the project.')
    else:
        form = ProjectForm(instance=project)
    
    context = {
        'title' : 'Edit',
        'form': form,
        'project': project,
        'categories': categories,
    }
    return render(request, 'admin/front/main/project/edit.html', context)

@login_required(login_url='signIn')
@admin_role_required
def delete_project(request, slug):
        project = projectsSection.objects.filter(slug=slug)
        project.delete()
        messages.warning(request, 'Project deleted!')
        return redirect('projects')

# Admin Projects Category
@login_required(login_url='signIn')
@admin_role_required
def projectCategoryHome(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    project_categories = projectCategory.objects.filter(language__code=default_language_code)
    
    language_code = request.GET.get('language', default_language_code)
    
    if language_code:
        project_categories = projectCategory.objects.filter(language__code=language_code)
    
    context = {
        'title' : 'Projects Category',
        'project_categories': project_categories,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,  
        'default_language_code': default_language_code,
    }
    
    return render(request, 'admin/front/main/project/partial/category/category.html', context)

@login_required(login_url='signIn')
@admin_role_required
def createProjectCategory(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language', default_language_code)
    
    if request.method == 'POST':
        form = ProjectCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            project_category = form.save(commit=False)
            project_category.language = Languages.objects.get(code=language_code)
            project_category.save()
            messages.success(request, 'Category created successfully!')
            return redirect(reverse('projectCategories') + f'?language={language_code}')
    else:
        form = ProjectCategoryForm()
    context = {
        'title': 'Create Project Category',
        'form': form,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,  
        'default_language_code': default_language_code,
    }
    return render(request, 'admin/front/main/project/partial/category/create.html', context)

@login_required(login_url='signIn')
@admin_role_required
def editProjectCategory(request, slug):
        project_category = get_object_or_404(projectCategory, slug=slug)
        
        if request.method == 'POST':
            form = ProjectCategoryForm(request.POST, request.FILES, instance=project_category)
            if form.is_valid():
                form.save()
                messages.success(request, 'Category updated successfully!')
                return redirect(reverse('projectCategories') + f'?language={project_category.language.code}')
        else:
            form = ProjectCategoryForm(instance=project_category)
        
        context = {
            'title' : 'Edit',
            'form': form,
            'project_category': project_category,
        }
        return render(request, 'admin/front/main/project/partial/category/edit.html', context)

@login_required(login_url='signIn')
@admin_role_required
def deleteProjectCategory(request, slug):
        project_category = projectCategory.objects.filter(slug=slug)
        project_category.delete()
        messages.warning(request, 'Category deleted!')
        return redirect('projectCategories')

# Admin Testimonials Element
@login_required(login_url='signIn')
@admin_role_required
def testimonialHome(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    testimonials = testimonialsSection.objects.filter(language__code=default_language_code)
    
    Language_code = request.GET.get('language', default_language_code)
    
    if Language_code:
        testimonials = testimonialsSection.objects.filter(language__code=Language_code)
    
    context = {
        'title' : 'Testimonials',
        'testimonials': testimonials,
        'all_languages': Languages.objects.all(),
        'selected_language': Language_code,
        'default_language_code': default_language_code,
    }
    
    return render(request, 'admin/front/main/testimonial/testimonials.html', context)

@login_required(login_url='signIn')
@admin_role_required
def editTestimonial(request,slug):
    testimonial = get_object_or_404(testimonialsSection, slug=slug)
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial updated successfully!')
            return redirect(reverse('testimonials') + f'?language={testimonial.language.code}')
    else:
        form = TestimonialForm(instance=testimonial)
        
    context = {
        'title' : 'Edit',
        'form': form,
        'testimonial': testimonial,
    }
    return render(request, 'admin/front/main/testimonial/edit.html', context)

@login_required(login_url='signIn')
@admin_role_required
def createTestimonial(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    language_code = request.GET.get('language', default_language_code)
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
                testimonial = form.save(commit=False)
                testimonial.language = Languages.objects.get(code=language_code)
                testimonial.save()
                messages.success(request, 'Testimonial created successfully!')
                return redirect(reverse('testimonials') + f'?language={language_code}')
    else:
        form = TestimonialForm()

    context = {
        'title': 'Create Testimonial',
        'form': form,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,
        'default_language_code': default_language_code,
    }
    return render(request, 'admin/front/main/testimonial/create.html', context)

@login_required(login_url='signIn')
@admin_role_required
def deleteTestimonial(request, slug):
    testimonial = testimonialsSection.objects.filter(slug=slug)
    testimonial.delete()
    messages.warning(request, 'Testimonial deleted!')
    return redirect('testimonials')

# Admin Funfacts Element
@login_required(login_url='signIn')
@admin_role_required
def funfactHome(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    funfacts = funFactSection.objects.filter(language__code=default_language_code)
    
    language_code = request.GET.get('language', default_language_code)
    
    if language_code:
        funfacts = funFactSection.objects.filter(language__code=language_code)
    
    context = {
        'title' : 'Funfacts',
        'funfacts': funfacts,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,
        'default_language_code': default_language_code,
    }
    
    return render(request, 'admin/front/main/funfact/funfacts.html', context)

@login_required(login_url='signIn')
@admin_role_required
def editFunfact(request,slug):
    funfact = get_object_or_404(funFactSection, slug=slug)
    
    if request.method == 'POST':
        form = FunfactForm(request.POST, request.FILES, instance=funfact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fun fact updated successfully!')
            return redirect(reverse('funfacts') + f'?language={funfact.language.code}')
    else:
        form = FunfactForm(instance=funfact)
        
    context = {
        'title' : 'Edit',
        'form': form,
        'funfact': funfact,
    }
    return render(request, 'admin/front/main/funfact/edit.html', context)

@login_required(login_url='signIn')
@admin_role_required
def createFunfact(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    language_code = request.GET.get('language', default_language_code)
    
    if request.method == 'POST':
        form = FunfactForm(request.POST, request.FILES)
        if form.is_valid():
                funfact = form.save(commit=False)
                funfact.language = Languages.objects.get(code=language_code)
                funfact.save()
                messages.success(request, 'Fun fact created successfully!')
                return redirect(reverse('funfacts') + f'?language={language_code}')
    else:
        form = FunfactForm()

    context = {
        'title': 'Create Funfact',
        'form': form,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,
        'default_language_code': default_language_code,
    }
    return render(request, 'admin/front/main/funfact/create.html', context)

@login_required(login_url='signIn')
@admin_role_required
def deleteFunfact(request,slug):
    funfact = funFactSection.objects.filter(slug=slug)
    funfact.delete()
    messages.warning(request, 'Fun fact deleted!')
    return redirect('funfacts')

# Admin Team Member Element
@login_required(login_url='signIn')
@admin_role_required
def teamMemberHome(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    teams = teamSection.objects.filter(language__code=default_language_code)
    
    language_code = request.GET.get('language', default_language_code)
    
    if language_code:
        teams = teamSection.objects.filter(language__code=language_code)
    
    context = {
        'title' : 'Team Members',
        'teams': teams,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,
        'default_language_code': default_language_code,
    }
    
    return render(request, 'admin/front/main/team/team.html', context)
    
@login_required(login_url='signIn')
@admin_role_required
def editTeamMember(request,slug):
    team = get_object_or_404(teamSection, slug=slug)
    
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team updated successfully!')
            return redirect(reverse('teams') + f'?language={team.language.code}')
    else:
        form = TeamMemberForm(instance=team)
        
    context = {
        'title' : 'Edit',
        'form': form,
        'team': team,
    }
    return render(request, 'admin/front/main/team/edit.html', context)

@login_required(login_url='signIn')
@admin_role_required
def createTeamMember(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language', default_language_code)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
                team = form.save(commit=False)
                team.language = Languages.objects.get(code=language_code)
                team.save()
                messages.success(request, 'Team created successfully!')
                return redirect(reverse('teams') + f'?language={language_code}')
    else:
        form = TeamMemberForm()

    context = {
        'title': 'Create Team Member',
        'form': form,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,
        'default_language_code': default_language_code,
    }
    return render(request, 'admin/front/main/team/create.html', context)
    
@login_required(login_url='signIn')
@admin_role_required
def deleteTeamMember(request,slug):
    team = teamSection.objects.filter(slug=slug)
    team.delete()
    messages.warning(request, 'Team deleted!')
    return redirect('teams')

# Admin Clinet Element
@login_required(login_url='signIn')
@admin_role_required
def clientHome(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    clients = clientsSection.objects.filter(language__code=default_language_code)
    
    language_code = request.GET.get('language', default_language_code)
    
    if language_code:
        clients = clientsSection.objects.filter(language__code=language_code)
    
    context = {
        'title' : 'Clients',
        'clients': clients,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,
        'default_language_code': default_language_code,
    }
    
    return render(request, 'admin/front/main/client/clients.html', context)

@login_required(login_url='signIn')
@admin_role_required
def editClient(request,slug):
    client = get_object_or_404(clientsSection, slug=slug)
    
    if request.method == 'POST':
        form = ClientsForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client updated successfully!')
            return redirect(reverse('clients') + f'?language={client.language.code}')
    else:
        form = ClientsForm(instance=client)
        
    context = {
        'title' : 'Edit',
        'form': form,
        'client': client,
    }
    return render(request, 'admin/front/main/client/edit.html', context)
    
@login_required(login_url='signIn')
@admin_role_required
def createClient(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language', default_language_code)
    
    if request.method == 'POST':
        form = ClientsForm(request.POST, request.FILES)
        if form.is_valid():
                client = form.save(commit=False)
                client.language = Languages.objects.get(code=language_code)
                client.save()
                messages.success(request, 'Client created successfully!')
                return redirect(reverse('clients') + f'?language={language_code}')
    else:
        form = ClientsForm()

    context = {
        'title': 'Create Client',
        'form': form,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,
        'default_language_code': default_language_code,
    }
    return render(request, 'admin/front/main/client/create.html', context)

@login_required(login_url='signIn')
@admin_role_required
def deleteClient(request,slug):
    client = clientsSection.objects.filter(slug=slug)
    client.delete()
    messages.warning(request, 'Client deleted!')
    return redirect('clients')

# Admin Pricing Element
@login_required(login_url='signIn')
@admin_role_required
def adminPricingHome(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    pricingLists = pricing.objects.filter(language__code=default_language_code)
    
    language_code = request.GET.get('language', default_language_code)
    
    if language_code:
        pricingLists = pricing.objects.filter(language__code=language_code)
    context = {
        'title': 'Pricing',
        'pricingLists': pricingLists,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,
        'default_language_code': default_language_code,
    }
    return render(request, 'admin/front/main/pricing/pricing.html', context)

@login_required(login_url='signIn')
@admin_role_required
def editPricing(request, slug):
    pricingLists = get_object_or_404(pricing, slug=slug)
    
    if request.method == 'POST':
        form = PricingForm(request.POST, instance=pricingLists)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pricing updated successfully!')
            return redirect(reverse('pricing') + f'?language={pricingLists.language.code}')
    else:
        form = PricingForm(instance=pricingLists)
    context = {
        'title': 'Edit',
        'form': form,
        'pricing': pricingLists,
    }
    return render(request, 'admin/front/main/pricing/edit.html', context)

@login_required(login_url='signIn')
@admin_role_required
def createPricing(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language', default_language_code)
    
    if request.method == 'POST':
        form = PricingForm(request.POST)
        if form.is_valid():
            pricingLists = form.save(commit=False)
            pricingLists.language = Languages.objects.get(code=language_code)
            pricingLists.save()
            messages.success(request, 'Pricing created successfully!')
            return redirect(reverse('pricing') + f'?language={language_code}')
    else:
        form = PricingForm()
    context = {
        'title' : 'Create Pricing',
        'form' : form,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,
        'default_language_code': default_language_code,
    }
    return render(request, 'admin/front/main/pricing/create.html', context)

@login_required(login_url='signIn')
@admin_role_required
def deletePricing(request, slug):
    pricing_obj = get_object_or_404(pricing, slug=slug)
    pricing_obj.delete()
    messages.warning(request, 'Pricing deleted!')
    return redirect('pricing')

# Home Page Admin
@login_required(login_url='signIn')
@admin_role_required
def homeEditAdmin(request):
    
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language')
    
    if language_code:
        banner = bannerSection.objects.filter(language__code=language_code).first()
        homeSEO = HomePageSEO.objects.filter(language__code=language_code).first()
        service_section_title = serviceSectionTitle.objects.filter(language__code=language_code).first()
        project_section_title = projectSectionTitle.objects.filter(language__code=language_code).first()
        funfact_section_title = funFactSectionTitle.objects.filter(language__code=language_code).first()
        testimonial_section_title = testimonialSectionTitle.objects.filter(language__code=language_code).first()
        client_section_title = clientSectionTitle.objects.filter(language__code=language_code).first()
        blog_section_title = blogSectionTitle.objects.filter(language__code=language_code).first()
    else :
        homeSEO = HomePageSEO.objects.first()
        banner = bannerSection.objects.first()
        service_section_title = serviceSectionTitle.objects.first()
        project_section_title = projectSectionTitle.objects.first()
        funfact_section_title = funFactSectionTitle.objects.first()
        testimonial_section_title = testimonialSectionTitle.objects.first()
        client_section_title = clientSectionTitle.objects.first()
        blog_section_title = blogSectionTitle.objects.first()
        
    SeoForm = HomePageSEOForm(instance=homeSEO)
    form = BannerForm(instance=banner)
    service_section_title_form = serviceSectionTitleForm(instance=service_section_title)
    project_section_title_form = projectSectionTitleForm(instance=project_section_title)
    funfact_section_title_form = funFactSectionTitleForm(instance=funfact_section_title)
    testimonial_section_title_form = testimonialSectionTitleForm(instance=testimonial_section_title)
    client_section_title_form = clientSectionTitleForm(instance=client_section_title)
    blog_section_title_form = blogSectionTitleForm(instance=blog_section_title)

    
    if request.method == 'POST':
        if 'meta_title' in request.POST:
            SeoForm = HomePageSEOForm(request.POST, instance=homeSEO)
            if SeoForm.is_valid():
                homeSEO = SeoForm.save(commit=False)
                homeSEO.language = Languages.objects.get(code=language_code)
                homeSEO.save()
                messages.success(request, 'Home page seo updated successfully!')
                return redirect(reverse('homePageEditadm') + f'?language={language_code}')
        elif 'title' in request.POST:
            form = BannerForm(request.POST, request.FILES, instance=banner)
            if form.is_valid():
                banner = form.save(commit=False)
                banner.language = Languages.objects.get(code=language_code)
                banner.save()
                messages.success(request, 'Home page banner updated successfully!')
                return redirect(reverse('homePageEditadm') + f'?language={language_code}')
        elif 'service_section_title' in request.POST:
            service_section_title_form = serviceSectionTitleForm(request.POST, instance=service_section_title)
            if service_section_title_form.is_valid():
                service_section_title = service_section_title_form.save(commit=False)
                service_section_title.language = Languages.objects.get(code=language_code)
                service_section_title.save()
                messages.success(request, 'Service section title updated successfully!')
                return redirect(reverse('homePageEditadm') + f'?language={language_code}')
        elif 'project_section_title' in request.POST:
            project_section_title_form = projectSectionTitleForm(request.POST, instance=project_section_title)
            if project_section_title_form.is_valid():
                project_section_title = project_section_title_form.save(commit=False)
                project_section_title.language = Languages.objects.get(code=language_code)
                project_section_title.save()
                messages.success(request, 'Project section title updated successfully!')
                return redirect(reverse('homePageEditadm') + f'?language={language_code}')
        elif 'funfact_section_title' in request.POST:
            funfact_section_title_form = funFactSectionTitleForm(request.POST, instance=funfact_section_title)
            if funfact_section_title_form.is_valid():
                funfact_section_title = funfact_section_title_form.save(commit=False)
                funfact_section_title.language = Languages.objects.get(code=language_code)
                funfact_section_title.save()
                messages.success(request, 'Funfact section title updated successfully!')
                return redirect(reverse('homePageEditadm') + f'?language={language_code}')
        elif 'testimonial_section_title' in request.POST:
            testimonial_section_title_form = testimonialSectionTitleForm(request.POST, instance=testimonial_section_title)
            if testimonial_section_title_form.is_valid():
                testimonial_section_title = testimonial_section_title_form.save(commit=False)
                testimonial_section_title.language = Languages.objects.get(code=language_code)
                testimonial_section_title.save()
                messages.success(request, 'Testimonial section title updated successfully!')
                return redirect(reverse('homePageEditadm') + f'?language={language_code}')
        elif 'client_section_title' in request.POST:
            client_section_title_form = clientSectionTitleForm(request.POST, instance=client_section_title)
            if client_section_title_form.is_valid():
                client_section_title = client_section_title_form.save(commit=False)
                client_section_title.language = Languages.objects.get(code=language_code)
                client_section_title.save()
                messages.success(request, 'Client section title updated successfully!')
                return redirect(reverse('homePageEditadm') + f'?language={language_code}')
        elif 'blog_section_title' in request.POST:
            blog_section_title_form = blogSectionTitleForm(request.POST, instance=blog_section_title)
            if blog_section_title_form.is_valid():
                blog_section_title = blog_section_title_form.save(commit=False)
                blog_section_title.language = Languages.objects.get(code=language_code)
                blog_section_title.save()
                messages.success(request, 'Blog section title updated successfully!')
                return redirect(reverse('homePageEditadm') + f'?language={language_code}')
        else:
            return redirect('homePageEditadm')

    
    context = {
        'title': 'Edit Home Page',
        'SeoForm': SeoForm,
        'form' : form,
        'service_section_title_form' : service_section_title_form,
        'project_section_title_form' : project_section_title_form,
        'funfact_section_title_form' : funfact_section_title_form,
        'testimonial_section_title_form' : testimonial_section_title_form,
        'client_section_title_form' : client_section_title_form,
        'blog_section_title_form' : blog_section_title_form,
        'banner' : banner,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,  
        'default_language_code': default_language_code  
    }
        
    return render(request, 'admin/front/main/pages/home.html', context)


# About Page Admin
@login_required(login_url='signIn')
@admin_role_required
def aboutEditAdmin(request):
    about = aboutSettings.objects.first()
    aboutSEO = AboutPageSEO.objects.first()
    team_section_title = teamSectionTitle.objects.first()
    client_section_title = clientSectionTitle.objects.first()
    testimonial_section_title = testimonialSectionTitle.objects.first()
    
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language')
    
    if language_code:
        about = aboutSettings.objects.filter(language__code=language_code).first()
        aboutSEO = AboutPageSEO.objects.filter(language__code=language_code).first()
        team_section_title = teamSectionTitle.objects.filter(language__code=language_code).first()
        client_section_title = clientSectionTitle.objects.filter(language__code=language_code).first()
        testimonial_section_title = testimonialSectionTitle.objects.filter(language__code=language_code).first()
    
    if request.method == 'POST':
        if 'title_white' in request.POST:
            form = AboutPageForm(request.POST, request.FILES, instance=about)
            if form.is_valid():
                about = form.save(commit=False)
                about.language = Languages.objects.get(code=language_code)
                about.save()
                messages.success(request, 'About page updated successfully!')
                return redirect(reverse('aboutPageEditadm') + f'?language={language_code}')
            
        elif 'meta_title' in request.POST:
            seoForm = AboutPageSEOForm(request.POST, instance=aboutSEO)
            if seoForm.is_valid():
                aboutSEO = seoForm.save(commit=False)
                aboutSEO.language = Languages.objects.get(code=language_code)
                aboutSEO.save()
                messages.success(request, 'About page seo updated successfully!')
                return redirect(reverse('aboutPageEditadm') + f'?language={language_code}')
            
        elif 'team_section_title' in request.POST:
            team_section_title_form = teamSectionTitleForm(request.POST, instance=team_section_title)
            if team_section_title_form.is_valid():
                team_section_title = team_section_title_form.save(commit=False)
                team_section_title.language = Languages.objects.get(code=language_code)
                team_section_title.save()
                messages.success(request, 'Team section title updated successfully!')
                return redirect(reverse('aboutPageEditadm') + f'?language={language_code}')

        elif 'testimonial_section_title' in request.POST:
            testimonial_section_title_form = testimonialSectionTitleForm(request.POST, instance=testimonial_section_title)
            if testimonial_section_title_form.is_valid():
                testimonial_section_title = testimonial_section_title_form.save(commit=False)
                testimonial_section_title.language = Languages.objects.get(code=language_code)
                testimonial_section_title.save()
                messages.success(request, 'Testimonial section title updated successfully!')
                return redirect(reverse('aboutPageEditadm') + f'?language={language_code}')
            
        elif 'client_section_title' in request.POST:
            client_section_title_form = clientSectionTitleForm(request.POST, instance=client_section_title)
            if client_section_title_form.is_valid():
                client_section_title = client_section_title_form.save(commit=False)
                client_section_title.language = Languages.objects.get(code=language_code)
                client_section_title.save()
                messages.success(request, 'Client section title updated successfully!')
                return redirect(reverse('aboutPageEditadm') + f'?language={language_code}')
        else:
            return redirect('aboutPageEditadm')
        
    else:
        form = AboutPageForm(instance=about)
        seoForm = AboutPageSEOForm(instance=aboutSEO)
        team_section_title_form = teamSectionTitleForm(instance=team_section_title)
        client_section_title_form = clientSectionTitleForm(instance=client_section_title)
        testimonial_section_title_form = testimonialSectionTitleForm(instance=testimonial_section_title)
                                
    context = {
        'title': 'Edit About Page',
        'about': about,
        'form': form,
        'SeoForm': seoForm,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,  
        'default_language_code': default_language_code,
        'team_section_title_form' : team_section_title_form,
        'client_section_title_form' : client_section_title_form,
        'testimonial_section_title_form' : testimonial_section_title_form,
        
    }
           
    return render(request, 'admin/front/main/pages/about.html', context)

# Service Page Admin
@login_required(login_url='signIn')
@admin_role_required
def serviceEditAdmin(request):
    serviceSEO = ServicePageSEO.objects.first()
    service_section_title = serviceSectionTitle.objects.first()
    funfact_section_title = funFactSectionTitle.objects.first()
    
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language')
    
    if language_code:
        serviceSEO = ServicePageSEO.objects.filter(language__code=language_code).first()
        service_section_title = serviceSectionTitle.objects.filter(language__code=language_code).first()
        funfact_section_title = funFactSectionTitle.objects.filter(language__code=language_code).first()
        
    if request.method == 'POST':
        if 'meta_title' in request.POST:
            seoForm = ServicePageSEOForm(request.POST, instance=serviceSEO)
            if seoForm.is_valid():
                serviceSEO = seoForm.save(commit=False)
                serviceSEO.language = Languages.objects.get(code=language_code)
                serviceSEO.save()
                messages.success(request, 'Service page seo updated successfully!')
                return redirect(reverse('servicePageEditadm') + f'?language={language_code}')
        elif 'funfact_section_title' in request.POST:
            funfact_section_title_form = funFactSectionTitleForm(request.POST, instance=funfact_section_title)
            if funfact_section_title_form.is_valid():
                funfact_section_title = funfact_section_title_form.save(commit=False)
                funfact_section_title.language = Languages.objects.get(code=language_code)
                funfact_section_title.save()
                messages.success(request, 'Funfact section title updated successfully!')
                return redirect(reverse('servicePageEditadm') + f'?language={language_code}')
        elif 'service_section_title' in request.POST:
            service_section_title_form = serviceSectionTitleForm(request.POST, instance=service_section_title)
            if service_section_title_form.is_valid():
                service_section_title = service_section_title_form.save(commit=False)
                service_section_title.language = Languages.objects.get(code=language_code)
                service_section_title.save()
                messages.success(request, 'Service section title updated successfully!')
                return redirect(reverse('servicePageEditadm') + f'?language={language_code}')
    else:
        seoForm = ServicePageSEOForm(instance=serviceSEO)
        service_section_title_form = serviceSectionTitleForm(instance=service_section_title)
        funfact_section_title_form = funFactSectionTitleForm(instance=funfact_section_title)
        
    context = {
        'title': 'Edit Service Page',
        'seoForm' : seoForm,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,  
        'default_language_code': default_language_code,
        'service_section_title_form' : service_section_title_form,
        'funfact_section_title_form' : funfact_section_title_form,
    }
        
    return render(request, 'admin/front/main/pages/service.html', context)

# Pricing Page Admin
@login_required(login_url='signIn')
@admin_role_required
def pricingEditAdmin(request):
    seo = pricingPageSEO.objects.first()
    pricing_section_title = pricingSectionTitle.objects.first()
    
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language')
    
    if language_code:
        seo = pricingPageSEO.objects.filter(language__code=language_code).first()
        pricing_section_title = pricingSectionTitle.objects.filter(language__code=language_code).first()
        
    if request.method == 'POST':
        if 'meta_title' in request.POST:
            form = pricingPageSEOForm(request.POST, instance=seo)
            if form.is_valid():
                seo = form.save(commit=False)
                seo.language = Languages.objects.get(code=language_code)
                seo.save()
                messages.success(request, 'Pricing page seo updated successfully!')
                return redirect(reverse('pricingPageEditadm') + f'?language={language_code}')
        elif 'pricing_section_title' in request.POST:
            pricing_section_title_form = pricingSectionTitleForm(request.POST, instance=pricing_section_title)
            if pricing_section_title_form.is_valid():
                pricing_section_title = pricing_section_title_form.save(commit=False)
                pricing_section_title.language = Languages.objects.get(code=language_code)
                pricing_section_title.save()
                messages.success(request, 'Pricing section title updated successfully!')
                return redirect(reverse('pricingPageEditadm') + f'?language={language_code}')
            
    form = pricingPageSEOForm(instance=seo)
    pricing_section_title_form = pricingSectionTitleForm(instance=pricing_section_title)
        
    context = {
        'title' : 'Edit Pricing Page',
        'form' : form,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,  
        'default_language_code': default_language_code,
        'pricing_section_title_form' : pricing_section_title_form,
    }
    return render(request, 'admin/front/main/pages/pricing.html', context)

# Project Page Admin
@login_required(login_url='signIn')
@admin_role_required
def portfolioEditAdmin(request):
    portfolioSEO = PortfolioPageSEO.objects.first()
    project_section_title = projectSectionTitle.objects.first()
    
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language')
    
    if language_code:
        portfolioSEO = PortfolioPageSEO.objects.filter(language__code=language_code).first()
        project_section_title = projectSectionTitle.objects.filter(language__code=language_code).first()
        
    if request.method == 'POST':
        if 'meta_title' in request.POST:
            seoForm = PortfolioPageSEOForm(request.POST, instance=portfolioSEO)
            if seoForm.is_valid():
                portfolioSEO = seoForm.save(commit=False)
                portfolioSEO.language = Languages.objects.get(code=language_code)
                portfolioSEO.save()
                messages.success(request, 'Portfolio/Project page seo updated successfully!')
                return redirect(reverse('projectPageEditadm') + f'?language={language_code}')
        elif 'project_section_title' in request.POST:
            project_section_title_form = projectSectionTitleForm(request.POST, instance=project_section_title)
            if project_section_title_form.is_valid():
                project_section_title = project_section_title_form.save(commit=False)
                project_section_title.language = Languages.objects.get(code=language_code)
                project_section_title.save()
                messages.success(request, 'Project section title updated successfully!')
                return redirect(reverse('projectPageEditadm') + f'?language={language_code}')
    else:
        seoForm = PortfolioPageSEOForm(instance=portfolioSEO)
        project_section_title_form = projectSectionTitleForm(instance=project_section_title)
    context = {
        'title': 'Edit Portfolio Page',
        'seoForm' : seoForm,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,  
        'default_language_code': default_language_code,
        'project_section_title_form' : project_section_title_form,
    }
    return render(request, 'admin/front/main/pages/portfolio.html', context)

# Blog Page Admin
@login_required(login_url='signIn')
@admin_role_required
def blogPageAdmin(request):
    seo = blogPageSEO.objects.first()
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language')
    
    if language_code:
        seo = blogPageSEO.objects.filter(language__code=language_code).first()
        
    if request.method == 'POST':
        if 'meta_title' in request.POST:
            form = BlogPageSEOForm(request.POST, instance=seo)
            if form.is_valid():
                seo = form.save(commit=False)
                seo.language = Languages.objects.get(code=language_code)
                seo.save()
                messages.success(request, 'Blog page seo updated successfully!')
                return redirect(reverse('blogPageAdmin') + f'?language={language_code}')
    
    form = BlogPageSEOForm(instance=seo)
    
    context = {
        'title' : 'Edit Blog Page',
        'form' : form,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,
        'default_language_code': default_language_code,
    }
    
    return render(request, 'admin/front/main/pages/blog.html', context)
# Contact Page Admin
@login_required(login_url='signIn')
@admin_role_required
def contactEditAdmin(request):
    contactInfo = ContactInfo.objects.first()
    contactSEO = ContactPageSEO.objects.first()
    
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language')
    
    if language_code:
        contactInfo = ContactInfo.objects.filter(language__code=language_code).first()
        contactSEO = ContactPageSEO.objects.filter(language__code=language_code).first()

    form = ContactInfoForm(instance=contactInfo)
    SeoForm = ContactPageSEOForm(instance=contactSEO)

    if request.method == 'POST':
        if 'box1_title' in request.POST:
            form = ContactInfoForm(request.POST, instance=contactInfo)
            if form.is_valid():
                contactInfo = form.save(commit=False)
                contactInfo.language = Languages.objects.get(code=language_code)
                contactInfo.save()
                messages.success(request, 'Contact page updated successfully!')
                return redirect(reverse('contactPageEditadm') + f'?language={language_code}')
        elif 'meta_title' in request.POST:
            SeoForm = ContactPageSEOForm(request.POST, instance=contactSEO)
            if SeoForm.is_valid():
                contactSEO = SeoForm.save(commit=False)
                contactSEO.language = Languages.objects.get(code=language_code)
                contactSEO.save()
                messages.success(request, 'Contact page seo updated successfully!')
                return redirect(reverse('contactPageEditadm') + f'?language={language_code}')
        else:
            return redirect('contactPageEditadm')

    context = {
        'title': 'Edit Contact Page',
        'form': form,
        'seoForm' : SeoForm,
        'info' : contactInfo,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,  
        'default_language_code': default_language_code 
    }
    return render(request, 'admin/front/main/pages/contact.html', context)

@login_required(login_url='signIn')
def contactSubmissionsAdmin(request):
    contacts = contact.objects.all().order_by('-created_at')
    
    for contact_instance in contacts:
        message = contact_instance.message
        print(message)

    context = {
        'title': 'Contact Submissions',
        'page_obj': contacts,
    }
    return render(request, 'admin/front/main/pages/partial/contactsubmission.html', context)

@login_required(login_url='signIn')
@admin_role_required
def deleteSubmissionAdmin(request, id):
    contactData = contact.objects.filter(id=id)
    contactData.delete()
    messages.warning(request, 'Deleted successfully!')
    return redirect('contactSubmissionsadm')

# Admin Settings
@login_required(login_url='signIn')
@admin_role_required
def adminWebsiteSettings(request):
    websiteSettings = websiteSetting.objects.first()
    
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language', default_language_code)
    
    if language_code:
        websiteSettings = websiteSetting.objects.filter(language__code=language_code).first()
        
    if request.method == 'POST':
        settingForm = WebsiteSettingsForm(request.POST, request.FILES, instance=websiteSettings)
        if settingForm.is_valid():
            settings = settingForm.save(commit=False)
            settings.language = Languages.objects.get(code=language_code)
            settings.save()
            messages.success(request, 'System settings updated successfully!')
            return redirect(reverse('websiteSettingsadm') + f'?language={language_code}')
    else:
        settingForm = WebsiteSettingsForm(instance=websiteSettings)
        
    context = {
        'title': 'System Settings',
        'settings': websiteSettings,
        'settingForm': settingForm,
        'form': settingForm,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,
        'default_language_code': default_language_code,
    }
    return render(request, 'admin/front/main/settings/website.html', context)

@login_required(login_url='signIn')
@admin_role_required
def adminHeaderFooterSettings(request):
    headerFooterSettings = HeaderFooter.objects.first()
    
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language', default_language_code)
    
    if language_code:
        headerFooterSettings = HeaderFooter.objects.filter(language__code=language_code).first()
        
    if request.method == 'POST':
        form = HeaderFooterForm(request.POST, instance=headerFooterSettings)
        if form.is_valid():
            hf = form.save(commit=False)
            hf.language = Languages.objects.get(code=language_code)
            hf.save()
            messages.success(request, 'Header footer settings updated successfully!')
            return redirect(reverse('headerFooterSettingsadm') + f'?language={language_code}')
    else:
        form = HeaderFooterForm(instance=headerFooterSettings)
    
    context = {
        'title': 'Header Footer Settings',
        'form': form,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,
        'default_language_code': default_language_code,
    }
    return render(request, 'admin/front/main/settings/headerfooter.html', context)

@login_required(login_url='signIn')
@admin_role_required
def adminMenuSettings(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    menus = Menu.objects.filter(language__code=default_language_code)
    
    language_code = request.GET.get('language', default_language_code)
    
    if language_code:
        menus = Menu.objects.filter(language__code=language_code)
        
    context = {
        'title': 'Menu Settings',
        'menus': menus,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,
        'default_language_code': default_language_code,
    }
    return render(request, 'admin/front/main/settings/menu/menu.html', context)

@login_required(login_url='signIn')
@admin_role_required
def adminMenuCreate(request):
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language', default_language_code)
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            order = form.cleaned_data['order']
            language = Languages.objects.get(code=language_code)
            if Menu.objects.filter(order=order, language=language).exists():
                form.add_error('order', 'Order number already exists. Use a different order.')
            else:
                menu = form.save(commit=False)
                menu.language = Languages.objects.get(code=language_code)
                menu.save()
                messages.success(request, 'Menu item created successfully!')
                return redirect(reverse('menuSettingsadm') + f'?language={language_code}')
    else:
        form = MenuForm()
    context = {
        'title': 'Create Menu',
        'form': form,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,
        'default_language_code': default_language_code,
    }
    return render(request, 'admin/front/main/settings/menu/create.html', context)

@login_required(login_url='signIn')
@admin_role_required
def adminMenuEdit(request, slug):
    menu = get_object_or_404(Menu, slug=slug)
    
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            order = form.cleaned_data['order']
            language = Languages.objects.get(code=menu.language.code)
            if Menu.objects.exclude(slug=slug).filter(order=order, language=language).exists():
                form.add_error('order', 'Order number already exists. Use a different order.')
            else:
                form.save()
                messages.success(request, 'Menu item updated successfully!')
                return redirect(reverse('menuSettingsadm') + f'?language={menu.language.code}')
    else:
        form = MenuForm(instance=menu)
    
    context = {
        'title': 'Edit',
        'form' : form,
        'menu': menu,
    }
    return render(request, 'admin/front/main/settings/menu/edit.html', context)

@login_required(login_url='signIn')
@admin_role_required
def adminMenuDelete(request, slug):
    menu = Menu.objects.filter(slug=slug)
    menu.delete()
    messages.warning(request, 'Menu item deleted!')
    return redirect('menuSettingsadm')

@login_required(login_url='signIn')
@admin_role_required
def adminSEOSettings(request):
    SeoSettings = SeoSetting.objects.first()
    
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language', default_language_code)
    
    if language_code:
        SeoSettings = SeoSetting.objects.filter(language__code=language_code).first()
        
    if request.method == 'POST':
        form = SeoSettingForm(request.POST, request.FILES ,instance=SeoSettings)
        if form.is_valid():
            seo = form.save(commit=False)
            seo.language = Languages.objects.get(code=language_code)
            seo.save()
            messages.success(request, 'SEO settings updated successfully!')
            return redirect(reverse('seoSettingsadm') + f'?language={language_code}')
    else:
        form = SeoSettingForm(instance=SeoSettings)
    context = {
        'title': 'Seo Settings',
        'SeoSettings': SeoSettings,
        'form': form,
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,
        'default_language_code': default_language_code,
    }
    return render(request, 'admin/front/main/settings/seo.html', context)

# Error Page
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)
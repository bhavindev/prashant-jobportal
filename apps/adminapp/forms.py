from django import forms
from apps.settings.models import *
from apps.homepage.models import *
from apps.aboutpage.models import *
from apps.blog.models import *
from apps.servicepage.models import *
from apps.portfoliopage.models import *
from apps.contactpage.models import *
from apps.pricingpage.models import *

#Blog Form
class BlogForm(forms.ModelForm):
    class Meta:
        model = blogs
        fields = '__all__'
        exclude = ['language', 'category']
        widgets = {
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug' : forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'author' : forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

# Blog Category Form
class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = blogCategory
        fields = '__all__'
        exclude = ['language']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug' : forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

# Blog page seo Form
class BlogPageSEOForm(forms.ModelForm):
    class Meta:
        model = blogPageSEO
        fields = '__all__'
        exclude = ['language']
        widgets = {
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-control'}),
        }
# Service Form
class serviceForm(forms.ModelForm):
    class Meta:
        model = serviceSection
        fields = '__all__'
        exclude = ['language']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'})
        }

# Project Form
class ProjectForm(forms.ModelForm):
    class Meta:
        model = projectsSection
        fields = '__all__'
        exclude = ['language', 'category']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'button_text': forms.TextInput(attrs={'class': 'form-control'}),
            'button_url': forms.TextInput(attrs={'class': 'form-control'}),
            'order' : forms.NumberInput(attrs={'class': 'form-control'})
        }

# Project Category Form
class ProjectCategoryForm(forms.ModelForm):
    class Meta:
        model = projectCategory
        fields = '__all__'
        exclude = ['language']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Home Page Banner Form
class BannerForm(forms.ModelForm):
    class Meta:
        model = bannerSection
        fields = '__all__'
        exclude = ['language']
        widgets = {
            'show_quote_form' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description' : forms.Textarea(attrs={'rows':4})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# Testimonial Form
class TestimonialForm(forms.ModelForm):
    class Meta:
        model = testimonialsSection
        fields = '__all__'
        exclude = ['language']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'client_designation': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
# Funfact Form        
class FunfactForm(forms.ModelForm):
    class Meta:
        model = funFactSection
        fields = '__all__'
        exclude = ['language']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'fact_count': forms.TextInput(attrs={'class': 'form-control'}),
        }
            
# Team Member Form
class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = teamSection
        fields = '__all__'
        exclude = ['language']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'about' : forms.Textarea(attrs={'class' : 'form-control', 'rows' : 4}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Clients Form
class ClientsForm(forms.ModelForm):
    class Meta:
        model = clientsSection
        fields = '__all__'
        exclude = ['language']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_url': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Pricing Form
class PricingForm(forms.ModelForm):
    class Meta:
        model = pricing
        fields = '__all__' 
        exclude = ['language'] 
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'button_text' : forms.TextInput(attrs={'class': 'form-control'}),
            'button_url' : forms.TextInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'data-bs-original-title': '', 'title': ''}),
            'featured_badge_title': forms.TextInput(attrs={'class': 'form-control'}),
        }    

# Admin Pricing Page Forms
class pricingPageSEOForm(forms.ModelForm):
    class Meta:
        model = pricingPageSEO
        fields = '__all__'
        exlude = ['language']
        widgets = {
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Admin Home Page edit forms
# Home Page SEO Form
class HomePageSEOForm(forms.ModelForm):
    class Meta:
        model = HomePageSEO  # Specify the model class
        fields = '__all__'
        exclude = ['language']
        widgets = {
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-control'}),
        }
      
# Admin About Page edit forms
class AboutPageSEOForm(forms.ModelForm):
    class Meta:
        model = AboutPageSEO
        fields = '__all__'
        exclude = ['language']
        widgets = {
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AboutPageForm(forms.ModelForm):
    class Meta:
        model = aboutSettings
        fields = '__all__'
        exclude = ['language']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
# Admin Service Page Forms
class ServicePageSEOForm(forms.ModelForm):
    class Meta:
        model = ServicePageSEO
        fields = '__all__'
        exclude = ['language']
        widgets = {
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Admin Portfolio Page Forms
class PortfolioPageSEOForm(forms.ModelForm):
    class Meta:
        model = PortfolioPageSEO
        fields = '__all__'
        exlcude = ['language']
        widgets = {
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Admin Contact Page Forms
class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = '__all__'
        exclude = ['language']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ContactForm(forms.ModelForm):
    class Meta:
        model = contact
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'eg. Jhon Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder' : 'eg. name@gmail.com'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder' : 'eg. 12345678'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder' : 'Explain your thoughts'}),
        }

class ContactPageSEOForm(forms.ModelForm):
    class Meta:
        model = ContactPageSEO
        fields = '__all__'
        exclude = ['language']
        widgets = {
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Admin Settings Forms
class WebsiteSettingsForm(forms.ModelForm):
    def clean_primary_color(self):
        return self.cleaned_data['primary_color']

    def clean_link_color(self):
        return self.cleaned_data['link_color']

    def clean_wp_button_shed_color(self):
        return self.cleaned_data['wp_button_shed_color']
    class Meta:
        model = websiteSetting
        fields = '__all__'
        exclude = ['openai_api', 'max_token', 'is_enabled_for_user', 'language']
        widgets = {
            'hrm_attendance_clock_in_max_time': forms.TextInput(attrs={'class': 'form-control time-picker', 'id' : 'dpkr', 'type': 'time'}),
            'hrm_attendance_clock_out_min_time': forms.TextInput(attrs={'class': 'form-control time-picker', 'id' : 'dpkr2', 'type': 'time'}),
            'whatsapp_is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'id': 'whatsappSwitch'}),
            'messenger_is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'id': 'messengerSwitch'}),
            'default_menu_is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'id': 'menuSwitch'}),
            'is_search_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'id': 'searchSwitch'}),
            'primary_color': forms.TextInput(attrs={'id': 'primary_color_picker'}),
            'link_color': forms.TextInput(attrs={'id': 'link_color_picker'}),
            'wp_button_shed_color': forms.TextInput(attrs={'id': 'wp_button_shed_color_picker'}),
            'default_mode': forms.Select(attrs={'class': 'form-select'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            restrict_fields = ['hrm_attendance_clock_in_max_time', 'hrm_attendance_clock_out_min_time']
            if not field in restrict_fields:
                field.widget.attrs['class'] = 'form-control'
                
class HeaderFooterForm(forms.ModelForm):
    class Meta:
        model = HeaderFooter
        fields = '__all__'
        exclude = ['language']
        widgets = {
            'footer_layout' : forms.Select(attrs={'class': 'form-select'}),
            'what_to_show' : forms.Select(attrs={'class': 'form-select'}),
            'footer_small_text' : forms.Textarea(attrs={'rows':3}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        restrict_fields = ['what_to_show', 'footer_layout']
        
        for name, field in self.fields.items():
            if name not in restrict_fields:
                field.widget.attrs['class'] = 'form-control'


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'
        exclude = ['language']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
class SeoSettingForm(forms.ModelForm):
    class Meta:
        model = SeoSetting
        fields = '__all__'
        exclude = ['language']
        widgets = {
            'meta_description' : forms.Textarea(attrs={'rows':3}),
            'seo_keywords' : forms.Textarea(attrs={'rows':4, 'placeholder' : 'software,application,marketer,developer'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# Client Section Title Form
class clientSectionTitleForm(forms.ModelForm):
    class Meta:
        model = clientSectionTitle
        fields = '__all__'
        exclude = ['language']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# Testimonial Section Title Form
class testimonialSectionTitleForm(forms.ModelForm):
    class Meta:
        model = testimonialSectionTitle
        fields = '__all__'
        exclude = ['language']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# Project Section Title Form
class projectSectionTitleForm(forms.ModelForm):
    class Meta:
        model = projectSectionTitle
        fields = '__all__'
        exclude = ['language']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# Service Section Title Form         
class serviceSectionTitleForm(forms.ModelForm):
    class Meta:
        model = serviceSectionTitle
        fields = '__all__'
        exclude = ['language']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# Fun Fact Section Title Form          
class funFactSectionTitleForm(forms.ModelForm):
    class Meta:
        model = funFactSectionTitle
        fields = '__all__'
        exclude = ['language']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# Blog Section Title Form         
class blogSectionTitleForm(forms.ModelForm):
    class Meta:
        model = blogSectionTitle
        fields = '__all__'
        exclude = ['language']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
# Team Section Title Form
class teamSectionTitleForm(forms.ModelForm):
    class Meta:
        model = teamSectionTitle
        fields = '__all__'
        exclude = ['language']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
# Pricing Section Title Form
class pricingSectionTitleForm(forms.ModelForm):
    class Meta:
        model = pricingSectionTitle
        fields = '__all__'
        exclude = ['language']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

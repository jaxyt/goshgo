from django import forms
from .models import Site, Page, Shortcode

class SiteModelForm(forms.ModelForm):

    class Meta:
        model = Site
        #  fields = '__all__'
        fields = ('url', 'name', 'title', 'description', 'company_name', 'logo', 'metas', 'links', 'stylesheet',
            'header', 'auto_menu', 'menu', 'footer', 'scripts', 'custom_script',)
        widgets = {
            'url': forms.TextInput(),
            'name': forms.TextInput(),
            'title': forms.TextInput(),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 10}),
            'company_name': forms.TextInput(),
            'logo': forms.FileInput(),
            'metas': forms.Textarea(attrs={'class':'site-textarea-metas', 'cols': 50, 'rows': 10}),
            'links': forms.Textarea(attrs={'class':'site-textarea-links', 'cols': 50, 'rows': 10}),
            'stylesheet': forms.Textarea(attrs={'class':'site-textarea-style', 'cols': 50, 'rows': 10}),
            'header': forms.Textarea(attrs={'class':'site-textarea-header', 'cols': 50, 'rows': 10}),
            'auto_menu': forms.CheckboxInput(),
            'menu': forms.Textarea(attrs={'class':'site-textarea-menu', 'cols': 50, 'rows': 10}),
            'footer': forms.Textarea(attrs={'class':'site-textarea-footer', 'cols': 50, 'rows': 10}),
            'scripts': forms.Textarea(attrs={'class':'site-textarea-scripts', 'cols': 50, 'rows': 10}),
            'custom_script': forms.Textarea(attrs={'class':'site-textarea-js', 'cols': 50, 'rows': 10}),
        }


class MainSiteModelForm(forms.ModelForm):

    class Meta:
        model = Site
        #  fields = '__all__'
        fields = ('url', 'name', 'title', 'metas',)
        widgets = {
            'url': forms.TextInput(),
            'name': forms.TextInput(),
            'title': forms.TextInput(),
            'metas': forms.Textarea(attrs={'class':'site-textarea-metas', 'cols': 50, 'rows': 10}),
        }


class PageModelForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ('dynamic', 'route', 'name', 'extension', 'mime_type',
            'display_name', 'title', 'robots_meta', 'meta_description', 'metas', 'h_one', 'h_two',
            'content', 'custom_script', 'links', 'stylesheet', 'scripts', 'header', 'footer')
        widgets = {
            #'route': forms.Textarea(attrs={'cols': 10, 'rows': 1}),
            'dynamic': forms.CheckboxInput(),
            'route': forms.TextInput(),
            'name': forms.TextInput(),
            'extension': forms.TextInput(),
            'mime_type': forms.TextInput(),
            'display_name': forms.TextInput(),
            'title': forms.TextInput(),
            'robots_meta': forms.TextInput(),
            'meta_description': forms.Textarea(attrs={'class':'page-textarea-description', 'cols': 50, 'rows': 10}),
            'metas': forms.Textarea(attrs={'class':'page-textarea-metas', 'cols': 50, 'rows': 10}),
            'h_one': forms.Textarea(attrs={'class':'page-textarea-hone', 'cols': 50, 'rows': 10}),
            'h_two': forms.Textarea(attrs={'class':'page-textarea-htwo', 'cols': 50, 'rows': 10}),
            'content': forms.Textarea(attrs={'class':'page-textarea-content', 'cols': 50, 'rows': 20}),
            'custom_script': forms.Textarea(attrs={'class':'page-textarea-js', 'cols': 50, 'rows': 10}),
            'stylesheet': forms.Textarea(attrs={'class':'page-textarea-style', 'cols': 50, 'rows': 10}),
            'links': forms.Textarea(attrs={'cols': 50, 'rows': 10}),
            'scripts': forms.Textarea(attrs={'cols': 50, 'rows': 10}),
            'header': forms.Textarea(attrs={'cols': 50, 'rows': 10}),
            'footer': forms.Textarea(attrs={'cols': 50, 'rows': 10})

        }


class MainPageModelForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ('dynamic', 'route', 'name', 'extension', 'mime_type', 'display_name', 'title', 'content',)
        widgets = {
            #'route': forms.Textarea(attrs={'cols': 10, 'rows': 1}),
            'dynamic': forms.CheckboxInput(),
            'route': forms.TextInput(),
            'name': forms.TextInput(),
            'extension': forms.TextInput(),
            'mime_type': forms.TextInput(),
            'display_name': forms.TextInput(),
            'title': forms.TextInput(),
            'content': forms.Textarea(attrs={'class':'page-textarea-content', 'cols': 50, 'rows': 5}),

        }

class ShortcodeModelForm(forms.ModelForm):
    class Meta:
        model = Shortcode
        fields = '__all__'

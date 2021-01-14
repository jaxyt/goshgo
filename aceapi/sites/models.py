from django.db import models
from django.shortcuts import reverse
from django.core.validators import FileExtensionValidator
from profiles.models import Profile
from django.template.defaultfilters import slugify
# Create your models here.


class SiteManager(models.Manager):

    def get_unowned_sites(self, me):
        sites = Site.objects.all().exclude(owner=me)
        return sites


class Site(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='sites')
    url = models.TextField()
    name = models.TextField(blank=True, default="")
    title = models.TextField(blank=True, default="")
    description = models.TextField(blank=True, default="")
    #  represents = models.TextField(blank=True, default="company")
    company_name = models.TextField(blank=True, default="")
    logo = models.ImageField(blank=True, upload_to='logos', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    #  logo_url = models.TextField(blank=True, default="")
    #  logo_width = models.TextField(blank=True, default="")
    #  logo_height = models.TextField(blank=True, default="")
    #  logo_caption = models.TextField(blank=True, default="")
    #  search_url = models.TextField(blank=True, default="")
    #  twitter_username = models.TextField(blank=True, default="")
    #  twitter_card = models.TextField(blank=True, default="summary_large_image")
    #  facebook_url = models.TextField(blank=True, default="")
    #  linkedin_url = models.TextField(blank=True, default="")
    #  language = models.TextField(blank=True, default="en-US")
    #  char_set = models.TextField(blank=True, default="UTF-8")
    metas = models.TextField(blank=True, default="")
    links = models.TextField(blank=True, default="")
    stylesheet = models.TextField(blank=True, default="")
    header = models.TextField(blank=True, default="")
    auto_menu = models.BooleanField(default=False)
    menu = models.TextField(blank=True, default="")
    footer = models.TextField(blank=True, default="")
    scripts = models.TextField(blank=True, default="")
    custom_script = models.TextField(blank=True, default="")
    sitemap_link_count = models.IntegerField(blank=True, default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = SiteManager()

    def __str__(self):
        return str(self.title if self.title else self.url)

    def num_pages(self):
        return self.pages.all().count()

    def num_shortcodes(self):
        return self.shortcodes.all().count()

    def get_pages(self):
        return self.pages.all()

    def get_shortcodes(self):
        return self.shortcodes.all()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)


class PageManager(models.Manager):

    def get_unowned_pages(self, me):
        pages = Page.objects.all().exclude(publisher=me)
        return pages


class Page(models.Model):
    publisher = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='pages')
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='pages')
    #  canonical = models.TextField(blank=True, default="")
    robots_meta = models.TextField(blank=True, default="")
    meta_description = models.TextField(blank=True, default="")
    dynamic = models.BooleanField(default=False)
    pathpattern = models.TextField(blank=True, default="")
    route = models.TextField(blank=True, default="/")
    name = models.TextField()
    extension = models.TextField(blank=True, default=".html")
    mime_type = models.TextField(blank=True, default="text/html")
    title = models.TextField(blank=True, default="")
    h_one = models.TextField(blank=True, default="")
    h_two = models.TextField(blank=True, default="")
    display_name = models.TextField(blank=True, default="")
    content = models.TextField(blank=True, default="")
    draft = models.TextField(blank=True, default="")
    #  backup = models.TextField(blank=True, default="")
    metas = models.TextField(blank=True, default="")
    links = models.TextField(blank=True, default="")
    stylesheet = models.TextField(blank=True, default="")
    header = models.TextField(blank=True, default="")
    footer = models.TextField(blank=True, default="")
    scripts = models.TextField(blank=True, default="")
    custom_script = models.TextField(blank=True, default="")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = PageManager()

    def __str__(self):
        return str(self.title if self.title else f"{self.name if self.name else 'index'}{self.extension}")

    def num_shortcodes(self):
        return self.shortcodes.all().count()

    def get_shortcodes(self):
        return self.shortcodes.all()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)


class Shortcode(models.Model):
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, blank=True, null=True, related_name='shortcodes')
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, blank=True, null=True, related_name='shortcodes')
    mime_type = models.TextField(blank=True, default="text/plain")
    key = models.TextField()
    value = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.key} - {self.page.name if self.page else self.site.url if self.site else self.mime_type}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-key',)



    class Meta:
        ordering = ('-key',)

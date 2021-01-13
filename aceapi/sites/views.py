from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Site, Page, Shortcode
from profiles.models import Profile
from .forms import SiteModelForm, PageModelForm, ShortcodeModelForm
from django.forms import modelformset_factory
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

@login_required
def site_inline_edit(request, site_id):
    profile = Profile.objects.get(user=request.user)
    s = Site.objects.get(pk=site_id)
    pages = s.get_pages()
    rt = request.GET.get('route', '/index.html')
    def contains(list, filter):
        for x in list:
            if filter(x):
                return x
        return False
    page = contains(pages, lambda x: f"{x.route}{x.name}{x.extension}" == rt)
    if type(page) is bool:
        raise Http404("this page does not exist")
    context = {
        'profile': profile,
        'site': s,
        'page': page,
        'title': f"{page.title} - {s.title}",
        'stylesheet': f"{page.stylesheet}" if page.stylesheet != "" else f"{s.stylesheet}",
        'header': f"{page.header}" if page.header != "" else f"{s.header}",
        'footer': f"{page.footer}" if page.footer != "" else f"{s.footer}",

    }
    return render(request, 'sites/compile.html', context)

@login_required
def site_page_edit_view(request, site_id):
    profile = Profile.objects.get(user=request.user)
    site = Site.objects.get(pk=site_id)
    s_form = SiteModelForm(request.POST or None, instance=site, prefix='site')
    PageFormSet = modelformset_factory(Page, form=PageModelForm)

    if request.method == 'POST':
        formset = PageFormSet(request.POST, queryset=site.get_pages())
        if formset.is_valid() and s_form.is_valid():
            s_instance = s_form.save(commit=False)
            if not s_instance.owner:
                s_instance.owner = profile
            s_instance.save()
            p_instances = formset.save(commit=False)
            for instance in p_instances:
                if not instance.publisher:
                    instance.publisher = profile
                instance.site_id = site.id
                instance.save()

    formset = PageFormSet(queryset=site.get_pages())
    s_pages = site.get_pages()

    context = {
        's_form': s_form,
        'formset': formset,
        's_pages': s_pages
    }

    return render(request, 'sites/edit.html', context)


@login_required
def site_page_create_and_list_view(request):
    qs = Site.objects.all()
    profile = Profile.objects.get(user=request.user)

    # initials
    s_form = SiteModelForm()
    p_form = PageModelForm()
    site_added = False

    profile = Profile.objects.get(user=request.user)

    if 'submit_s_form' in request.POST:
        print(request.POST)
        s_form = SiteModelForm(request.POST, request.FILES)
        if s_form.is_valid():
            instance = s_form.save(commit=False)
            instance.owner = profile
            instance.save()
            s_form = SiteModelForm()
            site_added = True

    if 'submit_p_form' in request.POST:
        p_form = PageModelForm(request.POST)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.publisher = profile
            instance.site = Site.objects.get(id=request.POST.get('site_id'))
            instance.save()
            p_form = PageModelForm()


    context = {
        'qs': qs,
        'profile': profile,
        's_form': s_form,
        'p_form': p_form,
        'site_added': site_added,
    }

    return render(request, 'sites/main.html', context)




class SiteDeleteView(LoginRequiredMixin, DeleteView):
    model = Site
    template_name = 'sites/confirm_del.html'
    success_url = reverse_lazy('sites:main-site-view')
    # success_url = '/sites/'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Site.objects.get(pk=pk)
        if not self.request.user:
            messages.warning(self.request, 'You need to be the owner of the site in order to delete it')
        return obj

class SiteUpdateView(LoginRequiredMixin, UpdateView):
    form_class = SiteModelForm
    model = Site
    template_name = 'sites/update.html'
    success_url = reverse_lazy('sites:main-site-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You need to be the owner of the site in order to update it")
            return super().form_invalid(form)

class PageDeleteView(LoginRequiredMixin, DeleteView):
    model = Page
    template_name = 'pages/confirm_del.html'
    success_url = reverse_lazy('sites:main-site-view')
    # success_url = '/sites/'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Page.objects.get(pk=pk)
        if not self.request.user:
            messages.warning(self.request, 'You need to be the publisher of the page in order to delete it')
        return obj

class PageUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PageModelForm
    model = Page
    template_name = 'pages/update.html'
    success_url = reverse_lazy('sites:main-site-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You need to be the publisher of the page in order to update it")
            return super().form_invalid(form)

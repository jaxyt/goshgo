from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Site, Page, Shortcode
from profiles.models import Profile
from .forms import SiteModelForm, PageModelForm, ShortcodeModelForm, MainSiteModelForm, MainPageModelForm
from django.forms import modelformset_factory
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import re_path
from datetime import datetime
import re
# Create your views here.

def api_compiler(request, *args, **kwargs):
    site_id = kwargs['site_id']
    profile = None
    if request.user:
        profile = Profile.objects.get(user=request.user)
    s = Site.objects.get(pk=site_id)
    pages = s.get_pages()
    rt = request.GET.get('route', '/index.html')
    page = None
    vars = None
    for i in pages:
        if f"""{i.route}{i.name}{i.extension}""" == rt:
            page = i
        elif i.dynamic:
            if i.pathpattern:
                regx = re.compile(i.pathpattern)
                matched_route = re.match(regx, rt)
                if matched_route:
                    page = i
                    vars = matched_route.groupdict()
    if page is None:
        raise Http404("this page does not exist")

    context = {
        'profile': profile,
        'site': s,
        'page': page,
        'title': f"{page.title} - {s.title}",
        'pagestylesheet': True if page.stylesheet != "" else False,
        'pageheader': True if page.header != "" else False,
        'pagefooter': True if page.footer != "" else False,
        'pages': pages,

    }
    res = render(request, 'sites/response.html', context)
    if vars:
        print(vars)
    for i in s.attrs():
        if isinstance(i[1], (str, int, float, datetime)):
            regx = re.compile(f"XXsite__{i[0]}XX", re.MULTILINE)
            subbed = re.sub(regx, f"{i[1]}", res.content.decode('utf-8'))
            res.content = subbed.encode('utf-8')
    for i in page.attrs():
        if isinstance(i[1], (str, int, float, datetime)):
            regx = re.compile(f"XXpage__{i[0]}XX", re.MULTILINE)
            subbed = re.sub(regx, f"{i[1]}", res.content.decode('utf-8'))
            res.content = subbed.encode('utf-8')
    return res

@login_required
def site_inline_edit(request, *args, **kwargs):
    site_id = kwargs['site_id']
    profile = Profile.objects.get(user=request.user)
    s = Site.objects.get(pk=site_id)
    pages = s.get_pages()
    rt = request.GET.get('route', '/index.html')
    vars = None
    def contains(list, filter):
        for x in list:
            if filter(x):
                return x
            elif x.dynamic:
                regx = re.compile(x.pathpattern)
                matched_route = re.match(regx, rt)
                if matched_route:
                    vars = matched_route.groupdict()
                    return x
        return False
    page = contains(pages, lambda x: f"{x.route}{x.name}{x.extension}" == rt)
    if type(page) is bool:
        raise Http404("this page does not exist")
    s_form = SiteModelForm(request.POST or None, instance=s, prefix='site')
    p_form = PageModelForm(request.POST or None, instance=page, prefix='page')
    sites = Site.objects.all();

    #for i in s.attrs():
    #    print(i)
    #for i in page.attrs():
    #    print(i)

    context = {
        'profile': profile,
        'site': s,
        'page': page,
        'title': f"{page.title} - {s.title}",
        'pagestylesheet': True if page.stylesheet != "" else False,
        'pageheader': True if page.header != "" else False,
        'pagefooter': True if page.footer != "" else False,
        's_form': s_form,
        'p_form': p_form,
        'sites': sites,
        'pages': pages,
        'permitted': '.html'

    }
    return render(request, 'sites/compile.html', context)


@login_required
def site_page_inline_ajax(request, site_id, page_id):
    profile = Profile.objects.get(user=request.user)
    data = {}
    site = Site.objects.get(pk=site_id)
    page = Page.objects.get(pk=page_id)
    s_form = SiteModelForm(request.POST or None, instance=site, prefix='site')
    p_form = PageModelForm(request.POST or None, instance=page, prefix='page')
    if request.method == 'POST':
        if s_form.is_valid() and p_form.is_valid():
            data['value'] = 'true'
            s_form.save()
            p_form.save()
        else:
            data['value'] = 'false'
    return JsonResponse(data, safe=False)


@login_required
def site_page_edit_view(request, site_id):
    profile = Profile.objects.get(user=request.user)
    site = Site.objects.get(pk=site_id)
    s_form = SiteModelForm(request.POST or None, instance=site, prefix='site')
    PageFormSet = modelformset_factory(Page, form=PageModelForm)
    data = {}
    if request.method == 'POST':
        #print(request.POST)
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
            data['value'] = 'true'
        else:
            data['value'] = 'false'
        return JsonResponse(data, safe=False)
    else:
        formset = PageFormSet(queryset=site.get_pages())
        s_pages = site.get_pages()

        context = {
            's_form': s_form,
            'formset': formset,
            's_pages': s_pages,
            'site': site,
        }

        return render(request, 'sites/edit.html', context)


@login_required
def site_page_create_and_list_view(request):
    qs = Site.objects.all()
    profile = Profile.objects.get(user=request.user)

    # initials
    s_form = MainSiteModelForm()
    p_form = MainPageModelForm()
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
        print(request.POST)
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

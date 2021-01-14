from django.urls import path
from .views import site_page_create_and_list_view, site_inline_edit, site_page_inline_ajax, site_page_edit_view, SiteDeleteView, SiteUpdateView, PageDeleteView, PageUpdateView

app_name = 'sites'

urlpatterns = [
    path('', site_page_create_and_list_view, name='main-site-view'),
    path('page/<pk>/delete/', PageDeleteView.as_view(), name='page-delete'),
    path('page/<pk>/update/', PageUpdateView.as_view(), name='page-update'),
    path('<pk>/delete/', SiteDeleteView.as_view(), name='site-delete'),
    path('<pk>/update/', SiteUpdateView.as_view(), name='site-update'),
    path('edit/<site_id>/', site_page_edit_view, name='site-edit'),
    path('inline/<site_id>/', site_inline_edit, name='site-inline'),
    path('published/<site_id>/<page_id>/', site_page_inline_ajax, name='site-page-ajax')

]

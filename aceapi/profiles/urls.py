from django.urls import path
from .views import (
    my_profile_view,
    profiles_list_view,
    ProfileDetailView,
    ProfileListView,
    signup,
    login_request,
    logout_request,
)

app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name='all-profiles-view'),
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('signup/', signup, name='signup'),
    path('login/', login_request, name='logn'),
    path('logout/', logout_request, name='log_out'),
    path('<slug>/', ProfileDetailView.as_view(), name='profile-detail-view'),
]

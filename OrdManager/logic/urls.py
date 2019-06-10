from django.urls import path, include

from logic.views import MainPage, ToBuy, ChangeStaff

urlpatterns = [
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', MainPage.as_view(), name="main"),
    path('addbuy/', ToBuy.as_view(), name='addbuy'),
    path('changestaff/', ChangeStaff.as_view(), name='changestaff'),
]
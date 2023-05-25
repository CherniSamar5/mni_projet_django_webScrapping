from django.urls import path
from . import views
urlpatterns = [
    path('<int:pagination>',views.extractPhones , name = 'smartphoneParPages'),
    path('smartphone/', views.extractPhones, name='smartphone'),
    path('', views.extractPhones, name='extractPhones'),
    path('filter/', views.filterPhones, name='filterPhones'),

]
from django.urls import path
from . import views 


urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products),
    path('customer/', views.customer),
    path('people/', views.PersonListView.as_view()),
    path("netinfo/", views.netinfo, name="netinfo"), 
    path('datatable/', views.datatable_view, name='datatable'),
    path('images/<str:image_name>/', views.serve_image, name='serve_image'),
    # Add other URL patterns if you have any

]

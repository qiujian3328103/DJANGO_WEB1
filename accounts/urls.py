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
    path('form/', views.form_view, name='form'),
    path('form/<int:entry_id>/', views.form_view, name='edit_form'),
    path('datatable2/', views.datatable_view_form, name='datatable-view2'),
    path('data_json/', views.get_form_data_json, name='data_json'),
    path('delete_entry/', views.delete_entry, name='delete_entry'),
]

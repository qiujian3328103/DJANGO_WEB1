from django.urls import path
from . import views 


urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.home, name='home'),
    path('dashboard2/', views.chartjs_plot, name='chartjs_plot'),
    path('get_data/', views.get_data, name='get_data'),
    path('highchart/', views.highchart_plot, name='highchart_plot'),
    path('get_data_highchart/', views.get_data_highchart, name='get_data_highchart'),
    path('wafermap/', views.wafermap, name='wafermap'),
    
    # Add other URL patterns if you have any
    path('form/', views.form_view, name='form'),
    path('form/<int:entry_id>/', views.form_view, name='edit_form'),
    path('datatable2/', views.datatable_view_form, name='datatable-view2'),
    path('data_json/', views.get_form_data_json, name='data_json'),
    path('delete_entry/', views.delete_entry, name='delete_entry'),
    path('table_sparkline/', views.table_sparkline, name="table_sparkline"),
    path('data_json_sparkline/', views.get_sparkline_data, name='data_json_sparkline'),
    path('get_yield_data_for_modal/', views.get_data_for_table_modal, name='get_yield_data_for_modal'),
    path('list_view/', views.list_view, name='list_view'),
    path('get_bin_groups/', views.get_bin_groups_for_product, name='get_bin_groups_for_product'),
]

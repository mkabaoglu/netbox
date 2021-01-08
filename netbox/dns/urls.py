from django.urls import path

from extras.views import ObjectChangeLogView, ImageAttachmentEditView
from ipam.views import ServiceEditView
from . import views


app_name = 'dns'
urlpatterns = [
    path('zones/', views.ZoneListView.as_view(), name='zone_list'), 
    path('zones/add/', views.ZoneEditView.as_view(), name='zone_add'),
    path('zones/import/', views.ZoneListView.as_view(), name='zone_import'),
    path('zones/delete/', views.ZoneBulkDeleteView.as_view(), name='zone_bulk_delete'),
    path('zones/<int:pk>', views.ZoneView.as_view(), name='zone_view'),
    path('zones/<int:pk>/edit/', views.ZoneEditView.as_view(), name='zone_edit'),
    path('zones/<int:pk>/delete/', views.ZoneDeleteView.as_view(), name='zone_delete'),



    path('record/', views.RecordListView.as_view(), name='record_list'), 
    path('record/add/', views.RecordEditView.as_view(), name='record_add'),
    path('record/import/', views.RecordListView.as_view(), name='record_import'),
    path('record/delete/', views.RecordBulkDeleteView.as_view(), name='record_bulk_delete'),
    path('record/<int:pk>', views.RecordView.as_view(), name='record_view'),
    path('record/<int:pk>/edit/', views.RecordEditView.as_view(), name='record_edit'),
    path('record/<int:pk>/delete/', views.RecordDeleteView.as_view(), name='record_delete'),
]

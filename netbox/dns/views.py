'''
from collections import OrderedDict

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.db import transaction
from django.db.models import F, Prefetch
from django.forms import ModelMultipleChoiceField, MultipleHiddenInput, modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.views.generic import View

from circuits.models import Circuit
from extras.views import ObjectChangeLogView, ObjectConfigContextView
from ipam.models import IPAddress, Prefix, Service, VLAN
from ipam.tables import InterfaceIPAddressTable, InterfaceVLANTable

from secrets.models import Secret
from utilities.forms import ConfirmationForm
from utilities.paginator import EnhancedPaginator, get_paginate_count
from utilities.permissions import get_permission_for_model
from utilities.utils import csv_format, count_related
from utilities.views import GetReturnURLMixin, ObjectPermissionRequiredMixin
from virtualization.models import VirtualMachine
from . import filters, forms, tables
from .choices import DeviceFaceChoices
from .constants import NONCONNECTABLE_IFACE_TYPES
from .models import (
    Cable, CablePath, ConsolePort, ConsolePortTemplate, ConsoleServerPort, ConsoleServerPortTemplate, Device, DeviceBay,
    DeviceBayTemplate, DeviceRole, DeviceType, FrontPort, FrontPortTemplate, Interface, InterfaceTemplate,
    InventoryItem, Manufacturer, PathEndpoint, Platform, PowerFeed, PowerOutlet, PowerOutletTemplate, PowerPanel,
    PowerPort, PowerPortTemplate, Rack, RackGroup, RackReservation, RackRole, RearPort, RearPortTemplate, Region, Site,
    VirtualChassis,
)


class BulkDisconnectView(GetReturnURLMixin, ObjectPermissionRequiredMixin, View):
    """
    An extendable view for disconnection console/power/interface components in bulk.
    """
    queryset = None
    template_name = 'dcim/bulk_disconnect.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a new Form class from ConfirmationForm
        class _Form(ConfirmationForm):
            pk = ModelMultipleChoiceField(
                queryset=self.queryset,
                widget=MultipleHiddenInput()
            )

        self.form = _Form

    def get_required_permission(self):
        return get_permission_for_model(self.queryset.model, 'change')

    def post(self, request):

        selected_objects = []
        return_url = self.get_return_url(request)

        if '_confirm' in request.POST:
            form = self.form(request.POST)

            if form.is_valid():

                with transaction.atomic():

                    count = 0
                    for obj in self.queryset.filter(pk__in=form.cleaned_data['pk']):
                        if obj.cable is None:
                            continue
                        obj.cable.delete()
                        count += 1

                messages.success(request, "Disconnected {} {}".format(
                    count, self.queryset.model._meta.verbose_name_plural
                ))

                return redirect(return_url)

        else:
            form = self.form(initial={'pk': request.POST.getlist('pk')})
            selected_objects = self.queryset.filter(pk__in=form.initial['pk'])

        return render(request, self.template_name, {
            'form': form,
            'obj_type_plural': self.queryset.model._meta.verbose_name_plural,
            'selected_objects': selected_objects,
            'return_url': return_url,
        })

'''
#
# Zones
#

import mptt.managers
from django.views.generic import *
from . import filters, forms, tables
from netbox.views import generic
from .models import Zone,record


class ZoneListView(generic.ObjectListView):
    queryset = Zone.objects.all()
    #filterset = filters.ZoneFilterSet
    #filterset_form = forms.ZoneFilterForm
    table = tables.ZoneTable
    template_name='dns/zone_list.html'
    
class ZoneDeleteView(generic.ObjectDeleteView):
    queryset = Zone.objects.all()

class ZoneEditView(generic.ObjectEditView):
    queryset = Zone.objects.all()
    model_form = forms.ZoneForm
    template_name='dns/zone_edit.html'
class ZoneView(generic.ObjectView):
    queryset = Zone.objects.all()
    table = tables.ZoneTable
    template_name='dns/zone_view.html'

class ZoneBulkDeleteView(generic.BulkDeleteView):
    queryset = Zone.objects.all()
    table = tables.ZoneTable


#
# Zones
#

class RecordListView(generic.ObjectListView):
    queryset = record.objects.all()
    #filterset = filters.ZoneFilterSet
    #filterset_form = forms.ZoneFilterForm
    table = tables.recordTable
    template_name='dns/record_list.html'
    
class RecordDeleteView(generic.ObjectDeleteView):
    queryset = record.objects.all()

class RecordEditView(generic.ObjectEditView):
    queryset = record.objects.all()
    model_form = forms.recordForm
    template_name='dns/record_edit.html'
    
class RecordView(generic.ObjectView):
    queryset = record.objects.all()
    table = tables.recordTable
    template_name='dns/record_list.html'

class RecordBulkDeleteView(generic.BulkDeleteView):
    queryset = record.objects.all()
    table = tables.recordTable

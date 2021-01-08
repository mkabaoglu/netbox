from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from timezone_field import TimeZoneField
import CloudFlare
from dcim.choices import *
from dcim.constants import *
from dcim.fields import ASNField
from extras.models import ChangeLoggedModel, CustomFieldModel, ObjectChange, TaggedItem
from extras.utils import extras_features
from utilities.fields import NaturalOrderingField
from utilities.querysets import RestrictedQuerySet
from utilities.mptt import TreeManager
from utilities.utils import serialize_object
from utilities.choices import ChoiceSet
from django.core.exceptions import ObjectDoesNotExist

#
# Zones
#

class ZoneStatusChoices(ChoiceSet):

    
    STATUS_ACTIVE = 'active'
    STATUS_PASSIVE = 'passive'

    CHOICES = (
        (STATUS_ACTIVE, 'active'),
        (STATUS_PASSIVE, 'passive'),
    )

__all__ = (
    'Zone',
    'record'
)


#
# Zones
#

@extras_features('custom_fields', 'custom_links', 'export_templates', 'webhooks')
class Zone(ChangeLoggedModel, CustomFieldModel):
    
    name = models.CharField(
        max_length=100,
        unique=True
    )
   
    status = models.CharField(
        max_length=50,
        choices=ZoneStatusChoices,
        default=ZoneStatusChoices.STATUS_ACTIVE
    )

    objects = RestrictedQuerySet.as_manager()
    

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


    def get_status_class(self):
        return SiteStatusChoices.CSS_CLASSES.get(self.status)
    
    def get_absolute_url(self):
        return reverse('dns:zone_list')
    
    def zones_import():
        cf = CloudFlare.CloudFlare(token='4gs_1JGD4FQGAckttPfIerRuMp6W_sgfP-uSLg-c')
        zones = cf.zones.get(params = {'per_page':601})
        for zone in zones:
             zone_name = zone['name']
             try:
                 Zone.objects.get(name=zone_name)
             except  ObjectDoesNotExist:     
                 Zone.objects.create(name=zone_name)



#
# record
#

class RecordStatusChoices(ChoiceSet):

    
    Type_A = 'A'
    Type_Other = 'Other'

    CHOICES = (
        (Type_A ,'A'),
        (Type_Other , 'Other'),
    )
    CSS_CLASSES = {
        Type_A: 'succes',
        Type_Other: 'info',
        
    }
class TTLStatusChoices(ChoiceSet):

    
    TTL_auto = 'Auto'
    TTL_other = 'Other'

    CHOICES = (
        (TTL_auto ,'Auto'),
        (TTL_other , 'Other'),
    )
    CSS_CLASSES = {
        TTL_auto: 'succes',
        TTL_other: 'info',
        
    }

@extras_features('custom_fields', 'custom_links', 'export_templates', 'webhooks')
class record(ChangeLoggedModel, CustomFieldModel):
    
    r_name = models.CharField(
        max_length=100,
    )
   
    r_value = models.CharField(
        max_length=1000,
    )
    r_type = models.CharField(
        max_length=50,
        choices=RecordStatusChoices,
        default=RecordStatusChoices.Type_A
    )
    r_ttl=models.CharField(
        max_length=50,
        choices=TTLStatusChoices,
        default=TTLStatusChoices.TTL_auto
    )





    objects = RestrictedQuerySet.as_manager()
    

    class Meta:
        ordering = ('r_name',)

    def __str__(self):
        return self.r_name

    def get_r_type_class(self):
        return RecordStatusChoices.CSS_CLASSES.get(self.r_type)
    
    def get_r_ttl_class(self):
        return TTLStatusChoices.CSS_CLASSES.get(self.r_ttl)
   
    
    def get_absolute_url(self):
        return reverse('dns:record_list')
    
               
    def dns_record_import():
        cf = CloudFlare.CloudFlare(token='4gs_1JGD4FQGAckttPfIerRuMp6W_sgfP-uSLg-c')
        zones = cf.zones.get(params = {'per_page':1000})
        for zone in zones:
            for records in cf.zones.dns_records.get(zone['id'], params={'per_page':1000}):
                record.objects.create(r_name=records['name'],r_type=records['type'] ,r_value=records['content'])

        


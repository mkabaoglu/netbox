import django_tables2 as tables

from ..models import Zone,record
from utilities.tables import BaseTable, ButtonsColumn, ChoiceFieldColumn, TagColumn, ToggleColumn,LinkedCountColumn
from .template_code import Zone_Link,record_Link,record_Zone_link

__all__ = (

    'ZoneTable',
    'ZoneDetailTable',
    'recordTable'
    'recordDetailTable'
)



#
# Zones
#


class ZoneTable(BaseTable):
    pk = ToggleColumn()
    name = tables.TemplateColumn(
        template_code=Zone_Link,
        orderable=False,
    )
    status = ChoiceFieldColumn()
    
    class Meta(BaseTable.Meta):
        model = Zone
        fields = (
            'pk', 'name', 'status',
        )
        default_columns = ('pk', 'name', 'status',)
class ZoneDetailTable(ZoneTable):
    Zone_count = LinkedCountColumn(
        viewname='dns:Zone_list',
        url_params={'zone_id': 'pk'},
        verbose_name='Zones'
    )
    
    class Meta(ZoneTable.Meta):
        fields = (
            'pk', 'name','status',
        )
        default_columns = (
            'pk', 'name', 'status'
        )


#
# record
#

class recordTable(BaseTable):
    pk = ToggleColumn()
    
    r_name = tables.TemplateColumn(
        template_code=record_Link,
        orderable=False,
        verbose_name='Name'
    )
    
    r_type = tables.Column(verbose_name='Type')
    r_value=tables.Column(verbose_name='Value')
    r_ttl = tables.Column(verbose_name='TTL')
    
    class Meta(BaseTable.Meta):
        model = record
        fields = (
              'pk','r_name', 'r_type','r_value','r_ttl'
        )
        default_columns = ( 'pk', 'r_name','r_type','r_value','r_ttl')


class recordDetailTable(recordTable):
    record_count = LinkedCountColumn(
        viewname='dns:record_list',
        url_params={'record_id': 'pk'},
        verbose_name='records'
    )
    
    class Meta(recordTable.Meta):
        fields = (
             'pk','r_name', 'r_type','r_value','r_ttl'
        )
        default_columns = (
            'pk', 'r_name','r_type','r_value','r_ttl'
        )


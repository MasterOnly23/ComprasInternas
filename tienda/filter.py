from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _

from django.contrib.admin.widgets import AdminDateWidget

from datetime import datetime, timedelta

from django.db.models import Q

class FechaListFilter(SimpleListFilter):
    title = _('Fecha de creacion')
    parameter_name = 'fecha_creacion'

    def lookups(self, request, model_admin):
        return (
            ('hoy', _('Hoy')),
            ('ultimos7dias', _('Últimos 7 días')),
            ('ultimos30dias', _('Últimos 30 días')),
            ('rango', _('Rango de fechas')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'hoy':
            return queryset.filter(fecha_creacion=datetime.today().date())
        elif self.value() == 'ultimos7dias':
            return queryset.filter(fecha_creacion__gte=datetime.today().date() - timedelta(days=7))
        elif self.value() == 'ultimos30dias':
            return queryset.filter(fecha_creacion__gte=datetime.today().date() - timedelta(days=30))
        elif self.value() == 'rango':
            fecha_desde = request.GET.get('fecha_creacion__gte')
            fecha_hasta = request.GET.get('fecha_creacion__lte')
            if fecha_desde and fecha_hasta:
                    queryset = queryset.filter(
                        Q(fecha_creacion__gte=fecha_desde) &
                        Q(fecha_creacion__lte=fecha_hasta)
                    )
        return queryset




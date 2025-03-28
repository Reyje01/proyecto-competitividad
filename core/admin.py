from django.contrib import admin
from core.models import ValorCualitativo, ValorCuantitativo, Indicador, Pilar, UnidadAnalisis, Registro, IndiceIndicador, IndicePilar, IndiceGeneral, TipoUnidad


admin.site.register(TipoUnidad)

@admin.register(UnidadAnalisis)
class UnidadAnalisisAdmin(admin.ModelAdmin):
    list_display = ('nombre_unidad','provincia', 'idtipo_unidad')
    search_fields = ('nombre_unidad',)
    list_display_links = ('nombre_unidad',)
    list_filter = ('idtipo_unidad','provincia')
    list_per_page = 10 #paginacion

@admin.register(Pilar)
class PilarAdmin(admin.ModelAdmin):
    list_display = ('nombre_pilar', 'idtipo_unidad')
    search_fields = ('nombre_pilar',)
    list_display_links = ('nombre_pilar',)
    list_filter = ('idtipo_unidad',)
    list_per_page = 10 #paginacion

@admin.register(Indicador)
class IndicadorAdmin(admin.ModelAdmin):
    list_display = ('nombre_indicador','peso_indicador','tipo_indicador', 'idpilar')
    search_fields = ('nombre_indicador',)
    list_display_links = ('nombre_indicador',)
    list_filter = ('tipo_indicador', 'idpilar')
    list_per_page = 10 #paginacion

@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('idregistro','fecha_registro','idindicador', 'idunidad_analisis')
    search_fields = ('fecha_registro',)
    list_filter = ('idindicador', 'idunidad_analisis') 
    list_per_page = 10 #paginacion

@admin.register(ValorCuantitativo)
class ValorCuantitativoAdmin(admin.ModelAdmin):
    list_display = ('idregistro','valor_cuantitativo')
    search_fields = ('idregistro',)
    list_per_page = 10 #paginacion

@admin.register(ValorCualitativo)
class ValorCualitativoAdmin(admin.ModelAdmin):
    list_display = ('idregistro','valor_cualitativo')
    search_fields = ('idregistro',)
    list_per_page = 10 #paginacion

@admin.register(IndiceIndicador)
class IndiceIndicadorAdmin(admin.ModelAdmin):
    list_display = ('fecha_ii', 'valor_ii', 'clasificacion_ii', 'idindicador', 'idunidad_analisis')
    list_display_links = ('fecha_ii',)
    list_filter = ('idunidad_analisis',) 
    list_per_page = 10 #paginacion

@admin.register(IndicePilar)
class IndicePilarAdmin(admin.ModelAdmin):
    list_display = ('fecha_ip', 'valor_ip', 'clasificacion_ip', 'idpilar', 'idunidad_analisis')
    list_display_links = ('fecha_ip',)
    list_filter = ('idunidad_analisis',) 
    list_per_page = 10 #paginacion

@admin.register(IndiceGeneral)
class IndiceGeneralAdmin(admin.ModelAdmin):
    list_display = ('fecha_ig', 'valor_ig', 'clasificacion_ig', 'idunidad_analisis')
    list_display_links = ('fecha_ig',)
    list_filter = ('idunidad_analisis',) 
    list_per_page = 10 #paginacion
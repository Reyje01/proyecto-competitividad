from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from core.models import IndiceIndicador, IndicePilar, IndiceGeneral, Indicador, Pilar, UnidadAnalisis

@staff_member_required
def dashboard_view(request):
    # Filtros desde GET
    id_indicador = request.GET.get("id_indicador")
    id_unidad_analisis_indicador = request.GET.get("id_unidad_analisis_indicador")
    id_pilar = request.GET.get("id_pilar")
    id_unidad_analisis_pilar = request.GET.get("id_unidad_analisis_pilar")
    id_unidad_analisis_general = request.GET.get("id_unidad_analisis_general")

    # Base QuerySets
    indicadores = IndiceIndicador.objects.all()
    pilares = IndicePilar.objects.all()
    generales = IndiceGeneral.objects.all()

    # Aplicar filtros
    if id_indicador:
        indicadores = indicadores.filter(idindicador_id=id_indicador)
    if id_unidad_analisis_indicador:
        indicadores = indicadores.filter(idunidad_analisis_id=id_unidad_analisis_indicador)

    if id_pilar:
        pilares = pilares.filter(idpilar_id=id_pilar)
    if id_unidad_analisis_pilar:
        pilares = pilares.filter(idunidad_analisis_id=id_unidad_analisis_pilar)

    if id_unidad_analisis_general:
        generales = generales.filter(idunidad_analisis_id=id_unidad_analisis_general)

    # Preparar datos para charts
    def prepare_chart_data(queryset, fecha_field, valor_field):
        labels = [getattr(obj, fecha_field).strftime("%Y-%m-%d") for obj in queryset]
        values = [float(getattr(obj, valor_field) or 0) for obj in queryset]
        return {"labels": labels, "values": values}

    context = {
        "data_indicador": prepare_chart_data(indicadores.order_by("fecha_ii"), "fecha_ii", "valor_ii"),
        "data_pilar": prepare_chart_data(pilares.order_by("fecha_ip"), "fecha_ip", "valor_ip"),
        "data_general": prepare_chart_data(generales.order_by("fecha_ig"), "fecha_ig", "valor_ig"),
        "filter_fields": build_filter_fields(request),
    }

    return render(request, "core/dashboard.html", context)

def build_filter_fields(request):
    return [
        {
            "name": "id_indicador",
            "label": "Indicador",
            "options": [
                {"id": obj.idindicador, "name": obj.nombre_indicador}
                for obj in Indicador.objects.all().order_by("nombre_indicador")
            ],
            "value": request.GET.get("id_indicador", ""),
        },
        {
            "name": "id_unidad_analisis_indicador",
            "label": "Unidad Análisis (Indicador)",
            "options": [
                {"id": obj.idunidad_analisis, "name": obj.nombre_unidad}
                for obj in UnidadAnalisis.objects.all().order_by("nombre_unidad")
            ],
            "value": request.GET.get("id_unidad_analisis_indicador", ""),
        },
        {
            "name": "id_pilar",
            "label": "Pilar",
            "options": [
                {"id": obj.idpilar, "name": obj.nombre_pilar}
                for obj in Pilar.objects.all().order_by("nombre_pilar")
            ],
            "value": request.GET.get("id_pilar", ""),
        },
        {
            "name": "id_unidad_analisis_pilar",
            "label": "Unidad Análisis (Pilar)",
            "options": [
                {"id": obj.idunidad_analisis, "name": obj.nombre_unidad}
                for obj in UnidadAnalisis.objects.all().order_by("nombre_unidad")
            ],
            "value": request.GET.get("id_unidad_analisis_pilar", ""),
        },
        {
            "name": "id_unidad_analisis_general",
            "label": "Unidad Análisis (General)",
            "options": [
                {"id": obj.idunidad_analisis, "name": obj.nombre_unidad}
                for obj in UnidadAnalisis.objects.all().order_by("nombre_unidad")
            ],
            "value": request.GET.get("id_unidad_analisis_general", ""),
        },
    ]

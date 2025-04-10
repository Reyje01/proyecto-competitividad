from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from core.models import IndiceIndicador, IndicePilar, IndiceGeneral, Indicador, Pilar, UnidadAnalisis
from django.db.models import Avg


def dashboard_data_api(request):
    from django.http import JsonResponse
    from django.db.models import Avg

    # Obtener filtros
    id_indicador = request.GET.get("id_indicador")
    id_unidad_analisis_indicador = request.GET.get("id_unidad_analisis_indicador")
    id_pilar = request.GET.get("id_pilar")
    id_unidad_analisis_pilar = request.GET.get("id_unidad_analisis_pilar")
    id_unidad_analisis_general = request.GET.get("id_unidad_analisis_general")

    # Base QuerySets
    indicadores = IndiceIndicador.objects.all()
    pilares = IndicePilar.objects.all()
    generales = IndiceGeneral.objects.all()

    # Aplicar filtros para gráficas de línea
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

    # Preparar datos para gráficas de línea
    def prepare_chart_data(queryset, fecha_field, valor_field):
        return {
            "labels": [getattr(obj, fecha_field).strftime("%Y-%m-%d") for obj in queryset],
            "values": [float(getattr(obj, valor_field) or 0) for obj in queryset],
        }

    # Preparar datos para gráficas de radar (solo filtrar por unidad de análisis correspondiente)
    def prepare_radar_data(queryset, group_field, value_field):
        data = (
            queryset
            .values(group_field)
            .annotate(promedio=Avg(value_field))
            .order_by(group_field)
        )
        labels = [item[group_field] for item in data]
        values = [round(item["promedio"] or 0, 2) for item in data]
        return {"labels": labels, "values": values}

    radar_data_indicador = prepare_radar_data(
        IndiceIndicador.objects.filter(idunidad_analisis_id=id_unidad_analisis_indicador),
        "idindicador__nombre_indicador",
        "valor_ii",
    ) if id_unidad_analisis_indicador else {"labels": [], "values": []}

    radar_data_pilar = prepare_radar_data(
        IndicePilar.objects.filter(idunidad_analisis_id=id_unidad_analisis_pilar),
        "idpilar__nombre_pilar",
        "valor_ip",
    ) if id_unidad_analisis_pilar else {"labels": [], "values": []}

    radar_data_general = prepare_radar_data(
        IndiceGeneral.objects.filter(idunidad_analisis_id=id_unidad_analisis_general),
        "idunidad_analisis__nombre_unidad",
        "valor_ig",
    ) if id_unidad_analisis_general else {"labels": [], "values": []}

    return JsonResponse({
        "data_indicador": prepare_chart_data(indicadores.order_by("fecha_ii"), "fecha_ii", "valor_ii"),
        "data_pilar": prepare_chart_data(pilares.order_by("fecha_ip"), "fecha_ip", "valor_ip"),
        "data_general": prepare_chart_data(generales.order_by("fecha_ig"), "fecha_ig", "valor_ig"),
        "radar_data_indicador": radar_data_indicador,
        "radar_data_pilar": radar_data_pilar,
        "radar_data_general": radar_data_general,
    })


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

    # Datos para radar (promedios por pilar de una unidad de análisis)
    radar_labels = []
    radar_values = []
    if id_unidad_analisis_general:
        promedio_pilares = (
            IndicePilar.objects
            .filter(idunidad_analisis_id=id_unidad_analisis_general)
            .values("idpilar__nombre_pilar")
            .annotate(promedio=Avg("valor_ip"))
            .order_by("idpilar__nombre_pilar")
        )
        radar_labels = [item["idpilar__nombre_pilar"] for item in promedio_pilares]
        radar_values = [round(item["promedio"], 2) if item["promedio"] is not None else 0 for item in promedio_pilares]

    context = {
        "data_indicador": prepare_chart_data(indicadores.order_by("fecha_ii"), "fecha_ii", "valor_ii"),
        "data_pilar": prepare_chart_data(pilares.order_by("fecha_ip"), "fecha_ip", "valor_ip"),
        "data_general": prepare_chart_data(generales.order_by("fecha_ig"), "fecha_ig", "valor_ig"),
        "filter_fields": build_filter_fields(request),
        "radar_data": {"labels": radar_labels, "values": radar_values},
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

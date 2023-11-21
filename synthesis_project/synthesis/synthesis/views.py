from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max

from .models import Project
from .models import ProjectTag

from .project_dao import get_all_projects

import json
import concurrent.futures
import time

@require_http_methods(["GET"])
def harvester_init(request):

    projects = get_all_projects()
    project_dict = {project.id: {
        'name': project.name,
        'poco': project.poco,
        'um': project.um,
        'link': project.link
        } for project in projects}

    return JsonResponse(project_dict, status=200)


# Verificar alternativa para esse decorator, pois diminui a segurança
@csrf_exempt
@require_http_methods(["GET", "POST"])
def comunication_harverster_synthesis(request):
    if request.method == "GET":
        # Consulta no banco de dados os dados que precisam de update
        update_list = {}

        for project in Project.objects.all():
            try:
                latest_row = ProjectTag.objects.filter(project_id=project.id).aggregate(Max('timestamp'))
                latest_time = latest_row['timestamp__max']
            except ProjectTag.DoesNotExist:
                latest_time = None
            update_list[project.id] = {
                "id": project.id,
                "link": project.link,
                "lastime": latest_time
            }

        return JsonResponse(update_list, status=200)
    elif request.method == "POST":
        # Obtém os dados do corpo da solicitação
        data = json.loads(request.body.decode("utf-8"))

        # Salva os dados no banco de dados
        for (key, inner_data) in data.items():
            temp = ProjectTag(project_id=key, data=inner_data['value'], timestamp=time.time())
            temp.save()
            # print(f"Project ID: {key}, value: {inner_data['value']}")

        purge_old_data()
        return JsonResponse({}, status=200)

# 1200 seconds = 20 minutes
def purge_old_data_for_project(project, keep_data_interval=1200):
    try:
        latest_row = ProjectTag.objects.filter(project_id=project.id).aggregate(Max('timestamp'))
        latest_time = latest_row['timestamp__max']
    except ProjectTag.DoesNotExist:
        latest_time = None
    for row in ProjectTag.objects.all():
        if latest_time and (row.timestamp < latest_time - keep_data_interval):
            if (row.project_id == project.id):
                row.delete()

def purge_old_data():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(purge_old_data_for_project, project) for project in Project.objects.all()]
        concurrent.futures.wait(futures)
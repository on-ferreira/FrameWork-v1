from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max

from .models import Project
from .models import ProjectData

import json
import concurrent.futures
import time

@require_http_methods(["GET"])
def harvester_init(request):
    # projects_mock = {
    #     "projeto1": {"id": 1, "name": "nome1", "poco": "poco1", "um": "um1", "link": "link_dados1"},
    #     "projeto2": {"id": 2, "name": "nome2", "poco": "poco2", "um": "um2", "link": "link_dados2"},
    # }

    if (not Project.objects.filter(id=1).exists()):
        p1 = Project(name="Project 1", poco="Poco 1", um="UM 1", link="https://api.chucknorris.io/jokes/random")
        p2 = Project(name="Project 2", poco="Poco 2", um="UM 2", link="https://api.chucknorris.io/jokes/random")
        # Other API Links
        # p3 = Project(name="Project 3", poco="Poco 3", um="UM 3", link="https://uselessfacts.jsph.pl/api/v2/facts/random")
        # p4 = Project(name="Project 4", poco="Poco 4", um="UM 4", link="https://corporatebs-generator.sameerkumar.website/")

        p1.save()
        p2.save()
    
    projects = Project.objects.all()
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
                latest_row = ProjectData.objects.filter(project_id=project.id).aggregate(Max('timestamp'))
                latest_time = latest_row['timestamp__max']
            except ProjectData.DoesNotExist:
                latest_time = None
            update_list[project.id] = {
                "id": project.id,
                "link": project.link,
                "lastime": latest_time
            }


        # id_Proj = 1
        # link_Proj = "https://api.chucknorris.io/jokes/random"
        # return JsonResponse({"proj1": {"id": id_Proj, "link": link_Proj, "Msg": "ultimos dados recebidos"}})
        return JsonResponse(update_list, status=200)
    elif request.method == "POST":
        # Obtém os dados do corpo da solicitação
        data = json.loads(request.body.decode("utf-8"))

        # Agora, você pode acessar os campos do corpo da solicitação
        # joke = data['1']["value"]

        # Salva os dados no banco de dados
        for (key, inner_data) in data.items():
            temp = ProjectData(project_id=key, data=inner_data['value'], timestamp=time.time())
            temp.save()
            # print(f"key: {key}, value: {inner_data['value']}")

        # print(f"dados recebidos: {joke}")
        purge_old_data()
        return JsonResponse({}, status=200)


def purge_old_data_for_project(project, keep_data_interval=1200):
    try:
        latest_row = ProjectData.objects.filter(project_id=project.id).aggregate(Max('timestamp'))
        latest_time = latest_row['timestamp__max']
    except ProjectData.DoesNotExist:
        latest_time = None
    for row in ProjectData.objects.all():
        if latest_time and (row.timestamp < latest_time - keep_data_interval):
            if (row.project_id == project.id):
                row.delete()

def purge_old_data():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(purge_old_data_for_project, project) for project in Project.objects.all()]
        concurrent.futures.wait(futures)

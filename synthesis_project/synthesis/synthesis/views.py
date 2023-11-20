from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Project


@require_http_methods(["GET"])
def harvester_init(request):
    # projects_mock = {
    #     "projeto1": {"id": 1, "name": "nome1", "poco": "poco1", "um": "um1", "link_dados_rto": "link_dados1"},
    #     "projeto2": {"id": 2, "name": "nome2", "poco": "poco2", "um": "um2", "link_dados_rto": "link_dados2"},
    # }

    # p1 = Project(name="Project 1", poco="Poco 1", um="UM 1", link_dados_rto="Link 1")
    # p2 = Project(name="Project 2", poco="Poco 2", um="UM 2", link_dados_rto="Link 2")
    p3 = Project(name="Project 3", poco="Poco 3", um="UM 3", link_dados_rto="Link 3")

    # p1.save()
    # p2.save()
    p3.save()

    projects = Project.objects.all()
    project_dict = {project.id: project.name for project in projects}
    print(project_dict)

    return JsonResponse(project_dict, status=200)


# Verificar alternativa para esse decorator, pois diminui a segurança
@csrf_exempt
@require_http_methods(["GET", "POST"])
def comunication_harverster_synthesis(request):
    if request.method == "GET":
        # Consulta no banco de dados os dados que precisam de update
        id_Proj = 1
        link_Proj = "https://api.chucknorris.io/jokes/random"
        return JsonResponse({"proj1": {"id": id_Proj, "link_dados_rto": link_Proj, "Msg": "ultimos dados recebidos"}})
    elif request.method == "POST":
        # Obtém os dados do corpo da solicitação
        data = json.loads(request.body.decode("utf-8"))

        # Agora, você pode acessar os campos do corpo da solicitação
        joke = data['1']["value"]

        # Salva os dados no banco de dados
        print(f"dados recebidos: {joke}")
        return JsonResponse({}, status=200)

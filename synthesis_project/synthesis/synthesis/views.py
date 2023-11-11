from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def harvester_init(request):
    projects_mock = {
        "projeto1": {"id": 1, "name": "nome1", "poco": "poco1", "um": "um1", "link_dados_rto": "link_dados1"},
        "projeto2": {"id": 2, "name": "nome2", "poco": "poco2", "um": "um2", "link_dados_rto": "link_dados2"},
                    }
    projects = projects_mock
    return JsonResponse(projects, status=200)


@require_http_methods(["GET", "POST"])
def comunication_harverster_synthesis(request):

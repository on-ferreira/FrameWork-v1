from .models import ProjectTag, Tags, Project
from datetime import datetime


def get_recent_value_for_project_and_tag(project_id, tag_id):
    """
    Retorna o valor mais recente para um projeto e tag específicos.
    """
    resultado = ProjectTag.objects.filter(projeto__id=project_id, tag__tag_id=tag_id).order_by('-timestamp').first()

    if resultado:
        return resultado.value
    else:
        return None


def get_oldest_value_for_project_and_tag(project_id, tag_id):
    """
    Retorna o valor mais antigo para um projeto e tag específicos.
    """
    resultado = ProjectTag.objects.filter(projeto__id=project_id, tag__tag_id=tag_id).order_by('timestamp').first()

    if resultado:
        return resultado.value
    else:
        return None


def get_project_tag_values_older_than(timestamp):
    """
    Retorna todos os valores da tabela ProjectTag com timestamp mais antiga que a timestamp especificada.
    """
    valores = ProjectTag.objects.filter(timestamp__lt=timestamp).values_list('value', flat=True)
    return list(valores)


def delete_project_tag_values_older_than(timestamp):
    """
    Exclui os registros da tabela ProjectTag com timestamp mais antiga que a timestamp especificada.
    """
    ProjectTag.objects.filter(timestamp__lt=timestamp).delete()


def get_all_tag_ids():
    """
    Retorna uma lista com os IDs de todas as tags.
    """
    tag_ids = Tags.objects.values_list('tag_id', flat=True)
    return list(tag_ids)


def get_all_projects():
    """
    Retorna todos os projetos.
    """
    return Project.objects.all()

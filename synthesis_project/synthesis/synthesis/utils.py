from .models import Project
from .models import Tags
from .project_dao import get_all_projects


def synthesis_init():
    projects = get_all_projects()
    if len(projects) == 0:
        p1 = Project(name="Project 1", poco="Poco 1", um="UM 1", link="https://link1.com")
        p2 = Project(name="Project 2", poco="Poco 2", um="UM 2", link="https://link2.com")

        p1.save()
        p2.save()

        t1 = Tags(tag_name="joke")
        t2 = Tags(tag_name="fact")
        t3 = Tags(tag_name="trivia")

        t1.save()
        t2.save()
        t3.save()

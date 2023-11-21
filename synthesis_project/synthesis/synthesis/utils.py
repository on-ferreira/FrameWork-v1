from .models import Project
from .models import Tags

def synthesis_init():
    if (not Project.objects.filter(id=1).exists()):
        p1 = Project(name="Project 1", poco="Poco 1", um="UM 1", link="https://link1.com")
        p2 = Project(name="Project 2", poco="Poco 2", um="UM 2", link="https://link2.com")

        p1.save()
        p2.save()

        t1 = Tags(name="joke")
        t2 = Tags(name="fact")
        t3 = Tags(name="trivia")

        t1.save()
        t2.save()
        t3.save()


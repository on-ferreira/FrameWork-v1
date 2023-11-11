from django.db import models
from sympy import true

#mudar depois para os padrões do sqlAlchemy
class Projeto(models.Model):
    name = models.CharField(max_length=255)
    poco = models.CharField(max_length=255)
    um = models.CharField(max_length=255)
    link_dados_rto = models.CharField(max_length=255)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "poco": self.poco,
            "um": self.um,
            "link_dados_rto": self.link_dados_rto,
        }
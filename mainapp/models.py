from django.db import models

# Create your models here.
class FooModel(models.Model):
    name = models.TextField()

    def _to_dict(self):
        return {"name": self.name}
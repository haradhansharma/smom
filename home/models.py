from django.db import models

# Create your models here.
class FeatureRequest(models.Model):
    wated_title = models.CharField(max_length=50)
    wanted = models.TextField(max_length=300)
    wanted_name = models.CharField(max_length=30)
    wanted_by = models.EmailField()
    requested = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.wanted
    

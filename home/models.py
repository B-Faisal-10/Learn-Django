from django.db import models
from PIL import Image

class Color(models.Model):
    color_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.color_name


class Person(models.Model):
    color = models.ForeignKey(Color,null=True, blank=True ,on_delete=models.CASCADE, related_name="color")
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    
    def __str__(self):
        return f"{self.name}"


class ImageModel(models.Model):
    image = models.ImageField(upload_to="persons/")


class MyImage(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
class Image(models.Model):
    my_image = models.ForeignKey(MyImage, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to='myImg/')

    def __str__(self):
        return self.image.name
    

class Statistics(models.Model):
    field_name = models.CharField(max_length=100)
    value = models.IntegerField()

    def __str__(self):
        return self.field_name
    
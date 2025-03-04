from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField('Название', max_length= 50)
    date = models.DateTimeField('Дата', unique=True)
    content = models.TextField('Содержимое')
    likes = models.IntegerField('Лайки', default=0)

    def __str__(self):
        return self.title

class GoogleUser(models.Model):
    google_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    profile_picture = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.email


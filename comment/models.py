from products.models import Product
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

def comment_validator(value):
    if len(value) < 5 or len(value) > 200:
        raise ValidationError('Yorum 5 karakterden kısa, 200 karakterden uzun olamaz.')

def rate_validator(value):
    if not isinstance(value,int) or (value < 1 or value > 5):
        raise ValidationError('Lütfen geçerli bir puan verin')

class Comment (models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    comment = models.TextField(max_length=200,validators=[comment_validator])
    rate = models.IntegerField(validators=[rate_validator])
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta():
        ordering = ['-create_at']


    def __str__(self):
        return self.user.username

    def save (self,*args,**kwargs):
        if not self.id:
            self.create_at = timezone.now()
        self.update_at = timezone.now()
        return super(Comment, self).save(*args,**kwargs)


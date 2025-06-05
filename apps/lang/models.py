from django.db import models
from django.core.exceptions import ValidationError

# Languages Creation Model
class Languages(models.Model):
    image = models.ImageField(upload_to='flags/', null=True, blank=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    is_rtl = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def clean(self):
        if Languages.objects.filter(name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError("A Languages with this name already exists.")
        if Languages.objects.filter(code=self.code).exclude(pk=self.pk).exists():
            raise ValidationError("A Languages with this code already exists.")

    def save(self, *args, **kwargs):
        if self.is_default:
            Languages.objects.exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
        
    def getFlag(self):
        return self.image.url if self.image else "https://media.istockphoto.com/id/1147544807/vector/thumbnail-image-vector-graphic.jpg?s=612x612&w=0&k=20&c=rnCKVbdxqkjlcs3xH87-9gocETqpspHFXu5dIGB4wuM="

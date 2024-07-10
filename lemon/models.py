from django.db import models

class Category(models.Model):
    slug=models.SlugField()
    title=models.CharField(max_length=255)
    def __str__(self):
        return self.title

class MenuItem(models.Model):
    Title=models.CharField(max_length=255)
    Price=models.DecimalField(max_digits=5,decimal_places=2)
    Inventory=models.SmallIntegerField()
    category=models.ForeignKey(Category,on_delete=models.PROTECT,default=1)

    def __str__(self):
        return self.Title



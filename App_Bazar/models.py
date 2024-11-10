from django.db import models
from django.db.models import Sum, F
from BAZAR_APP.settings import AUTH_USER_MODEL


# Create your models here.

class Category(models.Model):
    user= models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_category")
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Bazar(models.Model):
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author_bazar")
    name = models.CharField(max_length=264)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="bazar_category")
    per_kg_price = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(null=True, blank=True)
    publish_date = models.DateTimeField(auto_now_add = True)
    update_date = models.DateTimeField(auto_now = True)

    def total_cost(self):
        return round((self.per_kg_price * self.weight), 5)
    
    
    def all_bazar_cost(self):
        total = Bazar.objects.filter(author=self.author).aggregate(total_cost=Sum(F('per_kg_price') * F('weight')))['total_cost']
        return total or 0
    
    def __str__(self):
        return self.name
    

class Like(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_likes")
    bazar = models.ForeignKey(Bazar, on_delete=models.CASCADE, related_name="bazar_likes")

    def __str__(self):
        return f"{self.user} likes {self.bazar}"
    

class Comment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_comments")
    bazar = models.ForeignKey(Bazar, on_delete=models.CASCADE, related_name="bazar_comments")
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-comment_date']

    def __str__(self):
        return self.comment[:50]

class PendingBazar(models.Model):
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author_pending_bazar")
    name = models.CharField(max_length=264)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="pending_bazar_category")
    per_kg_price = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(null=True, blank=True)
    publish_date = models.DateTimeField(auto_now_add = True)
    update_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name
    

class Query(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'user_queries')
    query = models.CharField(max_length = 300)

    def __str__(self):
        return self.query[0:50]
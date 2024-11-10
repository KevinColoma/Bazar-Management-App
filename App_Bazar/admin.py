from django.contrib import admin
from App_Bazar.models import Category, Bazar, Like, Comment, PendingBazar, Query
# Register your models here.
admin.site.register(Category),
admin.site.register(Bazar),
admin.site.register(Like),
admin.site.register(Comment),
admin.site.register(PendingBazar),
admin.site.register(Query)

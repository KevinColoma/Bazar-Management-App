from django.forms import ModelForm
from App_Login.models import User, Profile
from App_Bazar.models import Category, Bazar, Comment, PendingBazar, Query

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ('user',)

class BazarForm(ModelForm):
    class Meta:
        model = Bazar
        exclude = ('author',)

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('user',)

class PendingBazarForm(ModelForm):
    class Meta:
        model = PendingBazar
        exclude = ('author',)


class QueryForm(ModelForm):
    class Meta:
        model = Query
        fields = ('query',)
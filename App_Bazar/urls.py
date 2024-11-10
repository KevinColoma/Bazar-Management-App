from django.urls import path
from App_Bazar import views
app_name = 'App_Bazar'

urlpatterns = [
    path('', views.home, name="home"),
    path('add-category/', views.add_category, name='add_category'),
    path('user-histories/', views.history, name='history'),
    path('edit_bazar/<pk>', views.edit_bazar, name="edit_bazar"),
    path('delete_bazar/<pk>', views.delete_bazar, name="delete_bazar"),
    path('others-bazar/<pk>', views.others_bazar, name='others_bazar'),
    path('user-cateogries', views.categories, name="user_categories"),
    path('update_category/<pk>', views.update_category, name="update_category"),
    path('delete_category/<pk>', views.delete_category, name="delete_category"),
    path('pending_bazars/', views.pending_bazars, name="pending_bazars"),
    path('update_pending_bazar/<pk>', views.update_pending_bazar, name="update_pending_bazar"),
    path('complete_pending_bazar/<pk>', views.complete_pending_bazar, name="complete_pending_bazar"),
    path('add_pending_bazar/', views.add_pending_bazar, name="add_pending_bazar"),
    path('bazar-history/', views.bazar_history, name="bazar_history"),
    path('bazar/<str:date>/', views.sorted_bazar, name='sorted_bazar'),
    path('query/', views.ask_ai, name="query"),
]
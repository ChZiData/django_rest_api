from django.urls import path
from api_basic import views

urlpatterns = [
    path('articels/', views.aritcle_list),
    path('articels/id=<int:pk>/', views.article_detail),
    path('zulassungen/marken=<str:marken>/', views.zulassungen_list),
    path('marken/', views.marken_list),
    
]
from django.urls import path

from webapp.views import index_view, create_article, article_view

urlpatterns = [
    path('', index_view, name="index"),
    path('articles/add/', create_article, name="create_article"),
    path('article/<int:pk>/', article_view, name="article_view")
]
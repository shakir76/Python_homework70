from django.urls import path

from webapp.views import index_view, create_article

urlpatterns = [
    path('', index_view),
    path('articles/add/', create_article)
]
from django.urls import path
from django.views.generic import RedirectView

from webapp.views import IndexView, CreateArticle, ArticleView, UpdateArticle, delete_article, CreateCommentView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('articles/', RedirectView.as_view(pattern_name="index")),
    path('articles/add/', CreateArticle.as_view(), name="create_article"),
    path('article/<int:pk>/', ArticleView.as_view(), name="article_view"),
    path('article/<int:pk>/update/', UpdateArticle.as_view(), name="update_article"),
    path('article/<int:pk>/delete/', delete_article, name="delete_article"),
    path('article/<int:pk>/comment/add/', CreateCommentView.as_view(), name="article_comment_create"),
]

from django.urls import path

from api_v1.views import ArticleView

app_name = 'api_v1'
urlpatterns = [
    path('articles/', ArticleView.as_view()),
    path('articles/<int:pk>/', ArticleView.as_view())

]
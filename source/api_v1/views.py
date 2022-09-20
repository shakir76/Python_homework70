from django.shortcuts import render

# Create your views here.
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from api_v1.serializers import ArticleModelsSerializer
from rest_framework.response import Response

from webapp.models import Article


class ArticleView(APIView):
    serializer_class = ArticleModelsSerializer

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            article = get_object_or_404(Article, pk=pk)
            article_data = self.serializer_class(article).data
            return Response(article_data)
        articles = Article.objects.all()
        articles_data = self.serializer_class(articles, many=True).data
        return Response(articles_data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def put(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=article)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response({'id': pk})

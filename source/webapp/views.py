from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.urls import reverse

# Create your views here.
from django.views import View

from webapp.forms import ArticleForm
from webapp.models import Article
from webapp.validate import article_validate
from django.views.generic import TemplateView, RedirectView


class IndexView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.order_by("-updated_at")
        context = {"articles": articles}
        return render(request, "index.html", context)


class MyRedirectView(RedirectView):
    url = "https://www.google.ru/"


class ArticleView(TemplateView):
    template_name = "article_view.html"

    # extra_context = {"test": "test"}
    # def get_template_names(self):
    #     return "article_view.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")
        article = get_object_or_404(Article, pk=pk)
        kwargs["article"] = article
        return super().get_context_data(**kwargs)


def create_article(request):
    if request.method == "GET":
        form = ArticleForm()
        return render(request, "create.html", {"form": form})
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            author = form.cleaned_data.get("author")
            content = form.cleaned_data.get("content")
            new_article = Article.objects.create(title=title, author=author, content=content)
            return redirect("article_view", pk=new_article.pk)
        return render(request, "create.html", {"form": form})


def update_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        form = ArticleForm(initial={
            "title": article.title,
            "author": article.author,
            "content": article.content
        })
        return render(request, "update.html", {"form": form})
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article.title = form.cleaned_data.get("title")
            article.author = form.cleaned_data.get("author")
            article.content = form.cleaned_data.get("content")
            article.save()
            return redirect("article_view", pk=article.pk)
        return render(request, "update.html", {"form": form})


def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        pass
    #     return render(request, "delete.html", {"article": article})
    else:
        article.delete()
        return redirect("index")

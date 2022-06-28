from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.urls import reverse

# Create your views here.
from webapp.models import Article


def index_view(request):
    articles = Article.objects.order_by("-updated_at")
    context = {"articles": articles}
    return render(request, "index.html", context)


def article_view(request, **kwargs):
    pk = kwargs.get("pk")
    article = get_object_or_404(Article, pk=pk)
    return render(request, "article_view.html", {"article": article})
    # try:
    #     article = Article.objects.get(pk=pk)
    # except Article.DoesNotExist:
    #     # return HttpResponseNotFound("Страница не найдена")
    #     raise Http404


def create_article(request):
    if request.method == "GET":
        return render(request, "create.html")
    else:
        title = request.POST.get("title")
        author = request.POST.get("author")
        content = request.POST.get("content")
        new_article = Article.objects.create(title=title, author=author, content=content)
        # print(reverse("article_view", kwargs={"pk": new_article.pk}))
        # return HttpResponseRedirect(reverse("article_view", kwargs={"pk": new_article.pk}))
        return redirect("article_view", pk=new_article.pk)
        # return HttpResponseRedirect(f"/article/{new_article.pk}")


def update_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        return render(request, "update.html", {"article": article})
    else:
        article.title = request.POST.get("title")
        article.author = request.POST.get("author")
        article.content = request.POST.get("content")
        article.save()
        return redirect("article_view", pk=article.pk)

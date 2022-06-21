from django.shortcuts import render


# Create your views here.
from webapp.models import Article


def index_view(request):
    articles = Article.objects.order_by("-created_at")
    context = {"articles": articles}
    return render(request, "index.html", context)


def create_article(request):
    if request.method == "GET":
        return render(request, "create.html")
    else:
        context = {
            "title": request.POST.get("title"),
            "author": request.POST.get("author"),
            "content": request.POST.get("content"),
        }
        return render(request, "article_view.html", context)

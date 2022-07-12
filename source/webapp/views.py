from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.urls import reverse

# Create your views here.
from django.views import View

from webapp.base_view import FormView as CustomFormView
from webapp.forms import ArticleForm
from webapp.models import Article
from webapp.validate import article_validate
from django.views.generic import TemplateView, RedirectView, FormView


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


class CreateArticle(CustomFormView):
    form_class = ArticleForm
    template_name = "create.html"

    def form_valid(self, form):
        tags = form.cleaned_data.pop("tags")
        self.article = Article.objects.create(**form.cleaned_data)
        self.article.tags.set(tags)
        return super().form_valid(form)

    def get_redirect_url(self):
        return redirect("article_view", pk=self.article.pk)


class UpdateArticle(FormView):
    form_class = ArticleForm
    template_name = "update.html"

    def dispatch(self, request, *args, **kwargs):
        self.article = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("article_view", kwargs={"pk": self.article.pk})

    def get_initial(self):
        initial = {}
        for key in 'title', 'content', 'author':
            initial[key] = getattr(self.article, key)
        initial['tags'] = self.article.tags.all()
        return initial

    def form_valid(self, form):
        tags = form.cleaned_data.pop('tags')
        # Article.objects.filter(pk=self.article.pk).update(**form.cleaned_data)
        for key, value in form.cleaned_data.items():
            setattr(self.article, key, value)
        self.article.save()
        self.article.tags.set(tags)
        return super().form_valid(form)

    def get_object(self):
        return get_object_or_404(Article, pk=self.kwargs.get("pk"))




def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        pass
    #     return render(request, "delete.html", {"article": article})
    else:
        article.delete()
        return redirect("index")

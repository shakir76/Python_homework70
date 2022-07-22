from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

# Create your views here.
from django.utils.http import urlencode

from webapp.views.base_view import FormView as CustomFormView
from webapp.forms import ArticleForm, SearchForm
from webapp.models import Article
from django.views.generic import TemplateView, RedirectView, FormView, ListView, DetailView


class IndexView(ListView):
    model = Article
    template_name = "articles/index.html"
    context_object_name = "articles"
    ordering = "-updated_at"
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Article.objects.filter(
                Q(author__icontains=self.search_value) | Q(title__icontains=self.search_value))
        return Article.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})  # search=dcsdvsdvsd
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class MyRedirectView(RedirectView):
    url = "https://www.google.ru/"


class ArticleView(DetailView):
    template_name = "articles/article_view.html"
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.order_by("-created_at")
        return context


class CreateArticle(CustomFormView):
    form_class = ArticleForm
    template_name = "articles/create.html"

    def form_valid(self, form):
        # tags = form.cleaned_data.pop("tags")
        # self.article = Article.objects.create(**form.cleaned_data)
        # self.article.tags.set(tags)
        self.article = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return redirect("article_view", pk=self.article.pk)


class UpdateArticle(FormView):
    form_class = ArticleForm
    template_name = "articles/update.html"

    def dispatch(self, request, *args, **kwargs):
        self.article = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("article_view", kwargs={"pk": self.article.pk})

    # def get_initial(self):
    #     initial = {}
    #     for key in 'title', 'content', 'author':
    #         initial[key] = getattr(self.article, key)
    #     initial['tags'] = self.article.tags.all()
    #     return initial
    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['instance'] = self.article
        return form_kwargs

    def form_valid(self, form):
        # tags = form.cleaned_data.pop('tags')
        # Article.objects.filter(pk=self.article.pk).update(**form.cleaned_data)
        # for key, value in form.cleaned_data.items():
        #     setattr(self.article, key, value)
        # self.article.save()
        # self.article.tags.set(tags)
        self.article = form.save()
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

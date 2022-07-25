from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView

from webapp.forms import CommentForm
from webapp.models import Article


class CreateCommentView(CreateView):
    form_class = CommentForm
    template_name = "comments/create.html"

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs.get("pk"))
        form.instance.article = article
        print(form.instance)
        return super().form_valid(form)


    # def form_valid(self, form):
    #     article = get_object_or_404(Article, pk=self.kwargs.get("pk"))
    #     comment = form.save(commit=False)
    #
    #     comment.article = article
    #     comment.save()
    #     form.save_m2m()
    #     return redirect("article_view", pk=article.pk)

    def get_success_url(self):
        return reverse("article_view", kwargs={"pk": self.object.article.pk})

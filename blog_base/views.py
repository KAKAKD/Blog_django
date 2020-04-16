from django.db.models import Count, Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect
from .models import Post, Category, Tag, Comment, Reply
from .form import CommentForm,ReplyForm
from django.contrib.auth.decorators import login_required


class PostDetailView(DetailView):
    model = Post
    template_name = 'detail.html'


    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj


class IndexView(ListView):
    model = Post
    template_name = 'index.html'
    paginate_by = 3


class CategoryListView(ListView):
    queryset = Category.objects.annotate(
        num_posts=Count('post', filter=Q(post__is_public=True)))


class TagListView(ListView):
    template_name = 'tag_list.html'
    queryset = Tag.objects.annotate(num_posts=Count(
        'post', filter=Q(post__is_public=True)))

class CategoryPostView(ListView):
    model = Post
    template_name = 'category_post.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class TagPostView(ListView):
    model = Post
    template_name = 'tag_post.html'

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        self.tag = get_object_or_404(Category, slug=tag_slug)
        qs = super().get_queryset().filter(category=self.tag)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context

class CommentFormView(CreateView):
    model = Comment
    template_name="base/comment_form.html"
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        post_pk = self.kwargs['pk']
        comment.post = get_object_or_404(Post, pk=post_pk)
        comment.save()
        return redirect('blog_base:detail', pk=post_pk)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['pk']
        context['post'] = get_object_or_404(Post,pk=post_pk)
        return context

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, post=pk)
    comment.approve()
    return redirect('blog_base:detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog_base:detail', pk=comment.post.pk)

class ReplyFormView(CreateView):
    model = Reply
    template_name="base/reply_form.html"
    form_class = ReplyForm

    def form_valid(self, form):
         reply = form.save(commit=False)
         comment_pk = self.kwargs['pk']
         reply.comment = get_object_or_404(Comment, pk=comment_pk)
         reply.save()
         return redirect('blog_base:detail', pk=reply.comment.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        context['comment'] = get_object_or_404(Comment, pk=comment_pk)
        return context

@login_required
def reply_approve(request, pk):
    reply = get_object_or_404(Reply,pk=pk)
    reply.approve()
    return redirect('blog_base:detail', pk=reply.comment.post.pk)

@login_required
def reply_remove(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply.delete()
    return redirect('blog_base:detail', pk=reply.comment.post.pk)

class SearchPostView(ListView):
    model = Post
    template_name='base/search_post.html'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q',None)
        lookup = (
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        )
        if query is not None:
            qs = super().get_queryset().filter(lookup).distinct()
            return qs
        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

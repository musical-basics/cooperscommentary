from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import (View, TemplateView,
                                ListView, DetailView,
                                CreateView, UpdateView,
                                DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

#below is a list of dictionaries
# posts = [
#     {
#         'author': 'CoreyMS',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'August 27, 2018'
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'August 28, 2018'
#     }
# ]

def home(request):
    #context assigns the dictionary posts to the key posts
    context = {
        'title': 'My awesome blog, check it out!',
        'posts':Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    #<app>/<model>_<viewtype>.html
    context_object_name = "posts"
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    #<app>/<model>_<viewtype>.html
    context_object_name = "posts"

    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

#loginrequiredmixin is used for authentication
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object() #this gets the exact post that we're editing
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    # return HttpResponse('<h1>Blog About</h1>')
    context = {
        'title':'About Page'
    }
    return render(request, 'blog/about.html', context)


############# Comments Section #############

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = CommentForm()

    return render(request, 'first_blog/comment_form.html', {'form':form})

@login_required
def comment_approved(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk = comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)





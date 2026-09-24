from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.http import require_POST
from .models import Post, Category
from django.db.models import F
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

def category_list(request, category):
    category = get_object_or_404(
        Category,
        slug = category
    )

    categories = Category.objects.all()

    posts = Post.published.filter(category=category)

    return render(
        request,
        'blog/category_list.html',
        {
            'categories' : categories,
            'category' : category,
            'posts' : posts
        }
    )

def post_detail(request, category, post):
    post = get_object_or_404(
        Post,
        category__slug__iexact=category,
        status = Post.Status.PUBLISHED,
        slug = post,
    )

    # active comments list
    comments = post.comments.filter(active = True)
    # form for comment
    form = CommentForm()

    Post.objects.filter(pk=post.pk).update(views=F('views') + 1)

    post.refresh_from_db()

    categories = Category.objects.all()

    return render(
        request,
        'blog/post/post_detail.html',
        {
            'categories' : categories,
            'post': post,
            'comments' : comments,
            'form' : form
        }
    )

def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status = Post.Status.PUBLISHED
    )

    sent = False

    categories = Category.objects.all()

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) recommends you read "
                f'"{post.title}"'
            )
            message = (
                f'Read "{post.title}" at {post_url}\n\n'
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject,
                message,
                'en4crypted@gmail.com',
                [cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/post_share.html',
        {
            'categories' : categories,
            'post': post,
            'form' : form,
            'sent' : sent,
        }
    )

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id = post_id,
        status = Post.Status.PUBLISHED
    )
    
    comment = None
    # comment was sent
    form = CommentForm(data = request.POST)
    if form.is_valid():
        # create object Comment, but not saving it to DB
        comment = form.save(commit = False)
        # make comment related to post
        comment.post = post
        # save object to DB
        comment.save()

    categories = Category.objects.all()

    return render(
        request,
        'blog/post/post_comment.html',
        {
            'post' : post,
            'form' : form,
            'comment' : comment,
            'categories' : categories
        }
    )

def home(request):
     posts = Post.published.all()

     categories = Category.objects.all()

     return render(
         request,
         'blog/home.html',
         {
             'posts' : posts,
             'categories' : categories
         }
     )

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.http import require_POST
from .models import Post, Category
from taggit.models import Tag
from django.db.models import F
from .forms import EmailPostForm, CommentForm, PostCreateForm

from django.contrib.auth import get_user_model

from django.core.mail import send_mail

from django.db.models import Count

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.conf import settings

from slugify import slugify

def post_list(request, category_slug = None, tag_slug = None):

    post_list = Post.published.select_related('category', 'author') # 1 request to DB

    category = None

    tag = None

    categories = Category.objects.all()

    if category_slug:
        category = get_object_or_404(
            Category,
            slug = category_slug
        )
        post_list = post_list.filter(category = category)

    elif tag_slug:
        tag = get_object_or_404(
            Tag,
            slug = tag_slug
        )
        post_list = post_list.filter(tags__in = [tag])

    else:
        post_list = Post.published.order_by('-publish')

    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(
        request,
        'feed/post_list.html',
        {
            'categories' : categories,
            'category' : category,
            'tag' : tag,
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

    # views logic

    Post.objects.filter(pk=post.pk).update(views=F('views') + 1)

    post.views += 1

    # similar posts list

    post_tags_ids = post.tags.values_list('id', flat = True)
    similar_posts = Post.published.select_related('category', 'author').filter(
        tags__in = post_tags_ids
    ).exclude(id = post.id)
    similar_posts = similar_posts.annotate(
        same_tags = Count('tags')
    ).order_by('-same_tags', '-publish')[:4]

    return render(
        request,
        'feed/post/post_detail.html',
        {
            'post': post,
            'comments' : comments,
            'form' : form,
            'similar_posts' : similar_posts
        }
    )

@login_required
def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status = Post.Status.PUBLISHED
    )

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{ request.user.username } ({ request.user.email }) recommends you read "
                f'"{post.title}"'
            )
            message = (
                f'Read "{post.title}" at {post_url}\n\n'
                f"{ request.user.username }\'s comments: {cd.get('comment', '')}"
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [cd['to']]
            )
            sent = True

            messages.success(
                request,
                'post was successfully shared via e-mail'
            )

        else:
            error_msg = '; '.join([f"{error}" for errors in form.errors.values() for error in errors]).lower()
            messages.error(
                request,
                f'error while sharing post: {error_msg}'
            )
    else:
        form = EmailPostForm()

    return render(
        request,
        'feed/post/post_share.html',
        {
            'post': post,
            'form': form
        }
    )

User = get_user_model()

@login_required
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id = post_id,
        status = Post.Status.PUBLISHED
    )

    form = CommentForm(data = request.POST)
    if form.is_valid():
        # create object Comment, but not saving it to DB
        comment = form.save(commit = False)
        # make comment related to post
        comment.post = post
        comment.user = request.user
        # save object to DB
        comment.save()
        messages.success(
            request,
            'comment was successfully published'
        )

    else:
        error_msg = '; '.join([f"{error}" for errors in form.errors.values() for error in errors]).lower()
        messages.error(
            request,
            f'error while publishing comment: {error_msg}'
        )

    return redirect(post.get_absolute_url())

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.status = Post.Status.PUBLISHED

            post.save()
            return redirect('feed:home')
    else:
        form = PostCreateForm()

    return render(
        request,
        'feed/post/post_create.html',
        {
            'form' : form
        }
    )

def home(request):
     posts = Post.published.all()

     return render(
         request,
         'feed/home.html',
         {
             'posts' : posts,
         }
     )

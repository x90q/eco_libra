from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.http import require_POST
from .models import Post, Category
from taggit.models import Tag
from django.db.models import F
from .forms import EmailPostForm, CommentForm, SearchForm

from django.contrib.postgres.search import (
    TrigramSimilarity,
    SearchVector,
    SearchQuery,
    SearchRank
)

from django.core.mail import send_mail

from django.db.models import Count

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
        'blog/post_list.html',
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
        'blog/post/post_detail.html',
        {
            'post': post,
            'comments' : comments,
            'form' : form,
            'similar_posts' : similar_posts
        }
    )

def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status = Post.Status.PUBLISHED
    )

    sent = False

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


    return render(
        request,
        'blog/post/post_comment.html',
        {
            'post' : post,
            'form' : form,
            'comment' : comment,
        }
    )

def home(request):
     posts = Post.published.all()

     return render(
         request,
         'blog/home.html',
         {
             'posts' : posts,
         }
     )

def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)

            result_list = Post.published.annotate(
            rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.1).order_by('-rank')

            if not result_list.exists():
                result_list = Post.published.annotate(
                    similarity=(
                    TrigramSimilarity('title', query) + 
                    TrigramSimilarity('body', query)
                    )
                ).filter(similarity__gt=0.05).order_by('-similarity')
            
            paginator = Paginator(result_list, 5)
            page_number = request.GET.get('page', 1)
            try:
                results = paginator.page(page_number)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)
            except PageNotAnInteger:
                results = paginator.page(1)               
            return render(
                request,
                'blog/post/search.html',
                {
                    'form' : form,
                    'query' : query,
                    'results' : results
                }
            )
    else:
        return redirect('blog:home')

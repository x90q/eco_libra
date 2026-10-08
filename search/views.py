from django.shortcuts import render, redirect, get_object_or_404
from .forms import SearchForm
from django.contrib.postgres.search import (
    TrigramSimilarity,
    SearchVector,
    SearchQuery,
    SearchRank
)
from feed.models import Post
from account.models import Profile
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.contrib.auth.decorators import login_required

from django.urls import reverse

from django.contrib.auth import get_user_model

def search_results(request):
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

            users_result_list = Profile.objects.annotate(
                similarity = (
                    TrigramSimilarity('user__username', query)
                )
            ).filter(similarity__gt=0.1).order_by('-similarity')[:7]

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
                'search/search_results.html',
                {
                    'form' : form,
                    'query' : query,
                    'results' : results,
                    'users' : users_result_list
                }
            )
    else:
        return redirect('feed:home')

@login_required
def posts_from_user(request, user_id):

    query = request.GET.get('query')

    if query:
        return redirect(f"{reverse('search:search_results')}?query={query}")

    User = get_user_model()

    posts_user = get_object_or_404(User, id=user_id)

    posts_list = posts_user.feed_posts.filter(status = Post.Status.PUBLISHED)

    paginator = Paginator(posts_list, 5)

    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)       

    return render(
        request,
        'search/posts_from_user.html',
        {
            'posts' : posts,
            'posts_user' : posts_user
        }
    )

def comments_from_user(request, user_id):

    User = get_user_model()

    comments_user = get_object_or_404(
        User,
        id = user_id
    )

    comments_list = comments_user.comments.filter(active = True)

    paginator = Paginator(comments_list, 5)
    page_number = request.GET.get('page', 1)

    try:
        comments = paginator.page(page_number)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        comments = paginator.page(1)

    return render(
        request,
        'search/comments_from_user.html',
        {
            'comments_user' : comments_user,
            'comments' : comments
        }
    )
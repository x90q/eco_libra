from django.shortcuts import render, redirect
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
            ).filter(similarity__gt=0.1).order_by('-similarity')[:8]

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

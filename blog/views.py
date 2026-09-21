from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.http import require_POST
from .models import Post
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

def post_list(request):
    post_list = Post.published.all()
    ### 5 Posts per page
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(
        request,
        'blog/post/post_list.html',
        {'posts': posts}
    )

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status = Post.Status.PUBLISHED,
        slug = post,
        publish__year = year,
        publish__month = month,
        publish__day = day
    )

    # active comments list
    comments = post.comments.filter(active = True)
    # form for comment
    form = CommentForm()

    return render(
        request,
        'blog/post/post_detail.html',
        {
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
            'comment' : comment
        }
    )

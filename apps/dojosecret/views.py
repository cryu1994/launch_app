from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Comment
from django.db.models import Count

def index(request):
    if 'user_id' in request.session:
        return redirect('/success')
    return render(request, "index/index.html")
# Create your views here.
def register(request):
    #because its short :P
    req = request.POST
    PostData = {
        'name': req['name'],
        'email': req['email'],
        'password': req['password'],
        'conf_password': req['conf_password']
    }
    #if there is no error returned
    if not User.objects.register(PostData):
        #then store new_user into a session so we could use it on the success page
        new_user_id = User.objects.create_user(PostData)
        request.session['user_id'] = new_user_id
        #then send it to the success page
        return redirect('/success/recent')
    #else if we got the errors as array, then display it and then redirect to the regi page
    for error in User.objects.register(PostData):
        messages.error(request, error)
    request.session['loginErr'] = False
    return redirect('/')
def login(request):
    req = request.POST
    PostData = {
        'email': req['email'],
        'password': req['password']
    }
    if not User.objects.login(PostData):
        user_id = User.objects.get(email=PostData['email']).id
        request.session['user_id'] = user_id
        return redirect('/success/recent')
    for error in User.objects.login(PostData):
        messages.error(request, error)
    request.session['loginErr'] = True
    return redirect('/')
def success(request, sort):
    if 'user_id' in request.session:
        user = User.objects.get(id = request.session['user_id'])
        if sort == 'recent':
            comments = Comment.objects.all().annotate(num_likes=Count('likes')).order_by('-created_at')[:5]
            alt_sort = "popular"
        elif sort == 'popular':
            comments = Comment.objects.all().annotate(num_likes=Count('likes')).order_by('-created_at')[:5]
            alt_sort = "recent"
        context = {
            'user': user,
            'comments': comments,
            'alt_sort': alt_sort,
            'sort': sort,
        }
        return render(request, "index/success.html", context)
    return redirect('/')
def create_comment(request):
    PostData = {
        'comment': request.POST['comment'],
        'user_id': request.session['user_id'],
    }
    Comment.objects.create_comment(PostData)
    return redirect('/success/recent')
def delete_comment(request, comment_id):
    if request.session['user_id'] == Comment.objects.get(id=comment_id).user.id:
        Comment.objects.delete_comment(comment_id)
    return redirect('/success/recent')
def popular(request):
    comment = Comment.objects.all().annotate(num_likes=Count(likes)).order_by('-num_likes')
    return redirect('/success/popular')
def like(request, comment_id):
    PostData = {
        'comment_id':comment_id,
        'user_id': request.session['user_id']
    }
    Comment.objects.like(PostData)
    return redirect('/success/recent')
def unlike(request, comment_id):
    PostData = {
        'comment_id':comment_id,
        'user_id':request.session['user_id']
    }
    Comment.objects.unlike(PostData)
    return redirect('/success/recent')
def logout(request):
    request.session.clear()
    return redirect('/')

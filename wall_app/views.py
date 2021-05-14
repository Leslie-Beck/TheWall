from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import *
# Create your views here.
def index(request):
    return render(request, 'index.html')

def create_user(request):
    if request.method == "POST":
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
            request.session['user_id'] = user.id
            print(user.password)
            print(request.session['user_id'])
            return redirect('/wall')
    return redirect('/')

def main_page(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'all_messages': Message.objects.all(),
        'all_comments': Comment.objects.all(),
    }
    return render(request, 'main_page.html', context)

def login(request):
    if request.method == "POST":
        users_with_email = User.objects.filter(email=request.POST['email'])
        if users_with_email:
            user = users_with_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                print(user.password)
                return redirect('/wall')
        messages.error(request, "email or password are not correct")
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')


def post_message(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        message = Message.objects.create(message=request.POST['message'], posted_by=User.objects.get(id=request.session['user_id']))
    return redirect('/wall')

def post_comment(request, post_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        poster = User.objects.get(id=request.session['user_id'])
        message = Message.objects.get(id=post_id)
        Comment.objects.create(comment=request.POST['comment'], posted_by=poster, posted_on=message)
    return redirect('/wall')



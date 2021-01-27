from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Wish, Granted_wish
import bcrypt


def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)

    if errors: 
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/')
    print('okie-dokie, doing good so far')

    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash
    )
    messages.info(request, 'You are in shape, go ahead and log in.')
    return redirect('/')

def login(request):
    
    try:
        user = User.objects.get(email = request.POST['email'])
    except:
        messages.error(request, 'You are trying wrong email or password.')
        return redirect('/')

    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        print('yay! password matches!')
    else:
        messages.error(request, 'Be informed that you are still using incorrect email or password.')
        return redirect('/')

    request.session['user_id'] = user.id
    request.session['first_name'] = user.first_name
    request.session['last_name'] = user.last_name
    request.session['email'] = user.email

    return redirect('/wishes')

def logout(request):
    del request.session['user_id']
    del request.session['first_name']
    del request.session['last_name']
    messages.info(request, 'You logged out! Come back soon!')
    return redirect('/')

def wishes(request):
    
        context = {
            'user': User.objects.get(email=request.session['email']),
            'wishes': User.objects.get(email=request.session['email']).wishes.all(),
            'granted_wishes': Granted_wish.objects.all()
        }
        return render(request, 'wishes.html', context)

def hacker(request):
    return render(request, 'hacker.html')

def new(request):
    
        context = {
            'user': User.objects.get(email=request.session['email'])
        }
        return render(request, 'new.html', context)

def edit(request, id):
    
        context = {
            'user': User.objects.get(email=request.session['email']),
            'wish': Wish.objects.get(id=id)
        }
        return render(request, 'edit.html', context)

def stats(request):
    
        context = {
            'user': User.objects.get(email=request.session['email']),
            'granted_wishes': Granted_wish.objects.count(),
            'user_granted_wishes': User.objects.get(email=request.session['email']).granted_wishes.count(),
            'user_pending_wishes': User.objects.get(email=request.session['email']).wishes.count()
        }
        return render(request, 'stats.html', context)

def new_wish(request):
    if request.method == 'POST':
        errors = Wish.objects.basic_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/new')
        else:
            Wish.objects.create(item=request.POST['item'], desc=request.POST['desc'], user=User.objects.get(
                id=request.POST['user_id']))
            return redirect('/wishes')
    else:
        return redirect('/')

def grant(request):
    if request.method == 'POST':
        Granted_wish.objects.create(item=request.POST['wish_item'], user=User.objects.get(
            id=request.POST['user_id']), date_added=request.POST['wish_created'])
        wish = Wish.objects.get(id=request.POST['wish_id'])
        wish.delete()
        return redirect('/wishes')
    else:
        return redirect('/')

def update(request, id):
    if request.method == 'POST':
        errors = Wish.objects.basic_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/edit/'+id)
        else:
            wish = Wish.objects.get(id=id)
            wish.item = request.POST['item']
            wish.desc = request.POST['desc']
            wish.save()
            return redirect('/wishes')
    else:
        return redirect('/')

def like(request):
    if request.method == 'POST':
        granted = Granted_wish.objects.get(id=request.POST['grant_id'])
        user = User.objects.get(id=request.POST['user_id'])
        if granted.user_id == user.id:
            messages.error(request, "Users may not like their own wishes.")
            return redirect('/wishes')
        if len(granted.likes.filter(id=request.POST['user_id'])) > 0:
            messages.error(request, "You have already liked this wish.")
            return redirect('/wishes')
        else:
            granted.likes.add(user)
            return redirect('/wishes')

def delete(request):
    if request.method == 'POST':
        wish = Wish.objects.get(id=request.POST['wish_id'])
        wish.delete()
        return redirect('/wishes')
    else:
        return redirect('/')

# def likes(request):
#     if('count' not in request.session):
#         request.session['likes'] = 'likes'
#     if (request.POST['likes'] == 'like'):
#         request.session['likes'] += 1
#     return redirect('/wishes')
from django.shortcuts import render,HttpResponseRedirect
from .models import Post
from .form import signupform,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html',{'posts':posts})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def signup(request):
    if request.method == 'POST':
        form = signupform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Signup successful')
    else:
        form = signupform()
    return render(request, 'blog/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            user = authenticate(username=uname, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in Successfully !!')
                return HttpResponseRedirect('/dashboard/')
            else:
                messages.error(request, 'Invalid Credentials')
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html',{'form':form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        fullname = user.get_full_name()
        return render(request, 'blog/dashboard.html',{'posts': posts,'fullname':fullname})
    else:
        return HttpResponseRedirect('/user_login/')

def delete_row(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
    
def edit_row(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = PostForm(request.POST,instance=Post.objects.get(pk=id))
            pi.save()
            messages.success(request, 'Post Updated Successfully!!')
            return HttpResponseRedirect('/dashboard/')
        else:
            form = PostForm(instance=Post.objects.get(pk=id))

            return render(request, 'blog/update.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def addpost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
          form = PostForm(request.POST)
          if form.is_valid:
            form.save()
            messages.success(request, 'Data added successfully!!!')
        else:
            form = PostForm()
    return render(request, 'blog/addpost.html', {'form': form})
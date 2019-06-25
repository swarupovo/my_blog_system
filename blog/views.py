import view as view
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
# from pymongo.auth import authenticate
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from blog.models import Post
from mysite_blog.settings import BLOG_TEMPLATE
from blog.form import PostForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User


def view_publish_blog(request):
    posts = Post.published.all()

    return render(request, BLOG_TEMPLATE + '/list.html', {"posts": posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day = day)
    return render(request, BLOG_TEMPLATE + '/detail.html', {'posts': post})


@login_required(login_url='/login/')
def post_form(request):
    print(request.method)
    if request.user.is_authenticated:
        if request.method == "POST":
            print("request in post method {}".format(request.method))
            form = PostForm(request.POST)
            print(form)
            print(type(form))
            if form.is_valid():
                try:
                    p = form.save()

                    messages.success(request, " form submited successfully")
                except:
                    messages.error(request, "somthing went wrong")
        return render(request, BLOG_TEMPLATE + "/blog_post.html", {'form': PostForm, 'name': request.user})






@csrf_exempt
def login_form(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            loginform = LoginForm(request.POST)
            if loginform.is_valid():
                data = request.POST.copy()

                username = data.get('username')
                password = data.get('password')
                confirm_password = data.get('confirm_password')

                print(username)
                print(password)
                print(confirm_password)
                try:
                    u = User.objects.get(username=username)
                    print(u.password)
                    if u:
                        user = authenticate(username=username, password=password)
                        if user is not None:
                            print("in if block")
                            login(request, user)
                            print(user)
                            messages.success(request, "you are successfully login")
                            return HttpResponseRedirect('/blog-list/blog/post/')
                        else:
                            messages.success(request, "you entered a wrong password ")

                    else:
                        messages.error(request, "you entered a wrong username")

                except Exception as E:
                    messages.error(request, "username is not valid")
            else:
                messages.error(request, loginform.errors)
            return render(request, BLOG_TEMPLATE + "/admin_login.html", {'login_form': LoginForm()})
        else:
            return render(request, BLOG_TEMPLATE + "/admin_login.html", {'login_form': LoginForm()})
    else:
        return HttpResponseRedirect('/blog-list/')


class Login_Form(View):
    formclass = LoginForm
    template = BLOG_TEMPLATE

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/blog-list/')
        else:
            return render(request, self.template + "/admin_login.html", {'login_form': self.formclass()})

    def post(self, request):
        loginform = self.formclass(request.POST)
        if loginform.is_valid():
            data = request.POST.copy()

            username = data.get('username')
            password = data.get('password')

            print(username)
            print(password)
            try:
                u = User.objects.get(username=username)
                print(u.password)
                if u:
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        print("in if block")
                        login(request, user)
                        print(user)
                        messages.success(request, "you are successfully login")
                        return HttpResponseRedirect('/blog-list/blog/post/')
                    else:
                        messages.success(request, "you entered a wrong password ")
                else:
                    messages.error(request, "you entered a wrong username")

            except Exception as E:
                messages.error(request, "username is not valid")
        else:
            messages.error(request, loginform.errors)
            return render(request, self.template + "/admin_login.html", {'login_form': self.formclass()})


class BlogList(ListView):

    template_name = BLOG_TEMPLATE + "/list.html"
    model = Post
    paginate_by = 1
    ordering = ['created']

@csrf_exempt
def logout_form(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('/login/')






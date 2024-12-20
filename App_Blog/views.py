from django.shortcuts import render,HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView,View
from App_Blog.models import Blog, Comment, Likes
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from App_Blog.forms import CommantForm
import uuid
import re
# Create your views here.

class CreateBlog(LoginRequiredMixin,CreateView):
    model = Blog
    template_name = 'App_Blog/create_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_image')
    
    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        # blog_obj.slug = title.replace(" ", "-") + "-" + str(uuid.uuid4())
        
        # Slugify the title and remove special characters
        blog_obj.slug = slugify(title) + "-" + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))

class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'App_Blog/blog_list.html'
    # queryset = Blog.objects.order_by('-publish_date')


@login_required
def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug) 
    comment_form = CommantForm()
    if request.method == 'POST':
        comment_form = CommantForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            comment_form = CommantForm()
            return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug':slug}))
    return render(request, 'App_Blog/blog_details.html', context={'blog':blog, 'comment_form':comment_form})

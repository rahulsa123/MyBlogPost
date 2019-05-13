from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Post #.models means current package
"""
dumy data 
posts = [
	{ 
		'author':"Rahul",
		"title":"Blog Post 1",
		"context" : "First post content",
		'date_update':"17/03/2019"	
	},
	{ 
		'author':"rohit",
		"title":"Blog Post 2",
		"context" : "Second post content",
		'date_update':"20/06/2019"	
	},
]"""

def home(request):
	context = {
	'posts': Post.objects.all()
	}
	return render(request, 'blog/home.html',context)

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['date_update'] # put '-' before name for reverse order

class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
	model = Post
	success_url = '/'  #home page 
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

def about(request):
	return render(request, 'blog/about.html',{'title' : "About"})


from django.shortcuts import render, redirect

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.urls import reverse_lazy
from .models import Task

# Create your views here.

# User
class CustomLogin(LoginView):
    template_name = 'TaskList/login.html'
    fields = '__all__'
    redirect_field_name = True
    
    def get_success_url(self):
        return reverse_lazy('task-list')


class RegisterPage(FormView):
    template_name = 'TaskList/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task-list')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task-list')
        return super(RegisterPage, self).get(*args, **kwargs)


# Tasks  
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'TaskList/tasks.html'
    context_object_name = 'task_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_list'] = context['task_list'].filter(user=self.request.user)
        context['count'] = context['task_list'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search') or ''
        if search_input:
            context['task_list'] =  context['task_list'].filter(title__startswith=search_input)
        
        context['search_input'] = search_input
        
        return context


class TaskDetail(DetailView):
    model = Task
    context_object_name = "task" 

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'TaskList/form.html'
    fields = {'title', 'description', 'priority', 'complete'}
    success_url = reverse_lazy('task-list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'TaskList/form.html'
    fields = {'complete', 'title', 'priority', 'description'}
    success_url = reverse_lazy("task-list")


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'TaskList/delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('task-list')
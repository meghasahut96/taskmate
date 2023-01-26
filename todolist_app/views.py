from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist_app.models import Todo
from .forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def todo(request):
  if request.method=="POST":
    form=TaskForm(request.POST or None)
    if form.is_valid():
      form.save(commit=False).manage=request.user
      form.save()
      messages.success(request,("Task added succesfully"))
    return redirect("todo")  
  else:
    all_task=Todo.objects.filter(manage=request.user)
    paginator=Paginator(all_task,5)
    page=request.GET.get('pg')
    all_task=paginator.get_page(page)
    context={'all_task':all_task}
    return render(request,"todolist_app/index.html",context)

@login_required
def delete_task(request,task_id):
  task=Todo.objects.get(pk=task_id)
  if task.manage==request.user:
    task.delete()
  else:
    messages.error(request,("Unauthorized to delete"))  
  return redirect("todo")

@login_required
def edit_task(request,task_id):
  if request.method=="POST":
    task=Todo.objects.get(pk=task_id)
    form=TaskForm(request.POST or None,instance=task)
    if form.is_valid():
      form.save()

    messages.success(request,("Task Edited"))
    return redirect("todo")  
  else:
    all_task=Todo.objects.get(pk=task_id)
    context={'all_task':all_task}
    return render(request,"todolist_app/edit.html",context)

@login_required
def complete_task(request,task_id):
  task=Todo.objects.get(pk=task_id)
  if task.manage==request.user:
    task.done=True
    task.save()
  else:
    messages.error(request,("Some error while changing"))
  return redirect("todo")

@login_required
def pending_task(request,task_id):
  task=Todo.objects.get(pk=task_id)
  task.done=False
  task.save()

  return redirect("todo")

def contact(request):
  return render(request,'todolist_app/contact.html')  
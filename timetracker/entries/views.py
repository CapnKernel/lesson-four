from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from .forms import ClientForm, EntryForm, ProjectForm
from .models import Client, Entry, Project


def clients(request):
    if request.method == 'POST':
        # If this view gets a POST request, it's an addition.
        # Create our form object with our POST data
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            # If the form is valid, let's create a Client with the submitted data
            client = Client()
            client.name = client_form.cleaned_data['name']
            client.save()
            messages.info(request, "New client '{}' created.".format(client.name))
            
            return HttpResponseRedirect(reverse('client-list'))
    else:
        client_form = ClientForm()

    client_list = Client.objects.all()
    return render(request, 'clients.html', {
        'client_list': client_list,
        'client_form': client_form,
    })


def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        # If this view gets a POST request, it's an edit.
        # Create our form object with our POST data
        form = ClientForm(request.POST)
        if form.is_valid():
            client.name = form.cleaned_data['name']
            client.save()
            messages.info(request, "Client '{}' saved.".format(client.name))

            return HttpResponseRedirect(reverse('client-list'))
    else:
        form = ClientForm(initial={'name': client.name})
        
    return render(request, 'client_detail.html', {
        'client_form': form,
    })

def entries(request):
    if request.method == 'POST':
        # Create our form object with our POST data
        entry_form = EntryForm(request.POST)
        if entry_form.is_valid():
            # If the form is valid, let's create and Entry with the submitted data
            project = get_object_or_404(Project, pk=entry_form.cleaned_data['project'])
            entry = Entry()
            entry.start = entry_form.cleaned_data['start']
            entry.stop = entry_form.cleaned_data['end']
            entry.project = project
            entry.description = entry_form.cleaned_data['description']
            entry.save()
    else:
        entry_form = EntryForm()

    entry_list = Entry.objects.all()
    return render(request, 'entries.html', {
        'entry_list': entry_list,
        'entry_form': entry_form,
    })

def entry_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'client_detail.html', {
        'client': client,
    })

def projects(request):
    if request.method == 'POST':
        # If this view gets a POST request, it's an addition.
        # Create our form object with our POST data
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            # If the form is valid, let's create a Project with the submitted data
            project = Project()
            project.name = project_form.cleaned_data['name']
            project.client = project_form.cleaned_data['client']
            project.save()
            messages.info(request, "New project '{}' created.".format(project.name))
    else:
        project_form = ProjectForm()

    project_list = Project.objects.all()
    return render(request, 'projects.html', {
        'project_list': project_list,
        'project_form': project_form,
    })

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        # If this view gets a POST request, it's an edit.
        # Create our form object with our POST data
        form = ProjectForm(request.POST)
        if form.is_valid():
            project.name = form.cleaned_data['name']
            project.client = form.cleaned_data['client']
            project.save()
            messages.info(request, "Project '{}' saved.".format(project.name))

            return HttpResponseRedirect(reverse('project-list'))
    else:
        form = ProjectForm(initial={'name': project.name, 'client': project.client})
        
    return render(request, 'project_detail.html', {
        'project_form': form,
    })

from email import message
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginationProjects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# What to do with the data that recieved, and where to go next from that page is what views is all about  


def projects(request):
    projects, search_query = searchProjects(request)
    # projects = Project.objects.all() # get all the Project list with all info abt it
    results = 6 # number of objects in a page
    custom_range, projects = paginationProjects(request, projects, results)
    context = {'projects': projects, 'search_query': search_query, 
                'custom_range': custom_range}

    return render(request, 'projects/projects.html', context)
 

def project(request, pk):
    projectObj = Project.objects.get(id=pk)  # get a particular project with id=pk
    # tags = projectObj.tags.all()  # get tags for that selected project to get many to many relations
    # reviews = projectObj.reviews.all()  # our class is Review but review_set is lowercase to get one to many relations
    #                                     # reviews is a related_name we gave in models.py. so, review_set wont work now
    form = ReviewForm()
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        messages.success(request, "Your review was successfully submitted!")

        projectObj.getVoteCount

        return redirect('project', pk=projectObj.id )
    context = {'project': projectObj, 'form': form}
        # 'tags': tags,
        # 'reviews': reviews}
    return render(request, 'projects/single-project.html', context)

# Creating the Project
@login_required(login_url="login")
def createProject(request):
    
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()

        form = ProjectForm(request.POST, request.FILES)  # request.FILES is to tell django the recieved data is with files
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project-form.html', context)

# Updating the Project\
@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')

    context = {'form': form, 'project': project}
    return render(request, 'projects/project-form.html', context)

# Deleting the Project
@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('account')
    return render(request, 'delete.html', {'object': project, 'pk': pk})



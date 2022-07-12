from django.db.models import Q
from .models import Project, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginationProjects(request, projects, results):
    page = request.GET.get('page')  # will throw an error bcz it doesnt know the page while first time visit
    paginator = Paginator(projects, results)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:   # for default page, PageNotANInteger is an error
        page = 1
        projects = paginator.page(page)
    except EmptyPage:      # if this error occurs, jst give us the last page
        page = paginator.num_pages  # number of pages, if we put the page no that doesnt exists
        projects = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages +1
    
    custom_range = range(leftIndex, rightIndex)
    return custom_range, projects


def searchProjects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    tags = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )
    return projects, search_query


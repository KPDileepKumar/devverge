from .models import Project,Tag
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def paginateProjects(request,projects,results):
    page=request.GET.get('page')
    paginator=Paginator(projects,results)
    try:
        projects=paginator.page(page)
    except PageNotAnInteger:
        page=1
        projects=paginator.page(page)
    except EmptyPage:
        page=paginator.num_pages
        projects=paginator.page(page)
    leftpage=int(page)-4
    if leftpage<1:
        leftpage=1
    rightpage=int(page)+5
    if rightpage>paginator.num_pages:
        rightpage=paginator.num_pages
    custom_range=range(leftpage,rightpage+1)
    return custom_range,projects


def searchProjects(request):
    search_query=""
    if request.GET.get('search_query'):
        search_query=request.GET.get('search_query')

    tags=Tag.objects.filter(name__contains=search_query)
    projects=Project.objects.distinct().filter(Q(title__icontains=search_query) | 
                                    Q(description__icontains=search_query) |
                                    Q(owner__name__icontains=search_query) |
                                    Q(tags__in=tags))
    return projects,search_query
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from projects.models import Project,Review
from .serializers import ProjectSerializer

@api_view(['GET'])
def getRoutes(request):
    routes=[
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},
        {'DELETE':'/api/projects/id'},

        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},
    ]
    return Response(routes)

@api_view(['GET'])

def getProjects(request):
    
    projects=Project.objects.all()
    serializer=ProjectSerializer(projects,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProject(request,pk):
    
    project=Project.objects.get(id=pk)
    serializer=ProjectSerializer(project,many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request,pk):
    project=Project.objects.get(id=pk)
    owner=request.user.profile
    data=request.data
    review,created=Review.objects.get_or_create(project=project,owner=owner)


    review.value=data["value"]
    review.save()
    project.getVoteRatio

    serializer=ProjectSerializer(project,many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteTag(request):
    tag_id=request.data['tag']
    project_id=request.data['project']
    project=Project.objects.get(id=project_id)
    tag=project.tags.get(id=tag_id)
    project.tags.remove(tag)
    return Response('Tag was deleted!')
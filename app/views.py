from rest_framework.response import Response
from rest_framework import generics
from . models import Post
from . serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated

# RetrieveAPIView - used for read-only endpoints to represent a single model instance.
# https://www.django-rest-framework.org/api-guide/generic-views/#retrieveapiview
class Postsview(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)  
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
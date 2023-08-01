from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import ProductSerializer, ScrapeSiteSerializer
from django_ratelimit.decorators import ratelimit
# Create your views here.


class ListProducts(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.request.user.products.all()


class ScrapeSite(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScrapeSiteSerializer

    @method_decorator(ratelimit(key='user_or_ip', rate='100/h'))
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from .producer import publish, send_all
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, User
from .serializers import ProductSerializer
import random


class ProductViewSet(viewsets.ViewSet):

    # /api/products/ #return list of objects [GET]
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        send_all('all_products', serializer.data)
        return Response(serializer.data)

    # /api/products/ #create new object [POST]
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish('product_created', serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # /api/products/<str:pk> #return one object [GET]
    def retrieve(self, request, pk=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    # /api/products/<str:pk> # update object by pk [PUT]
    def update(self, request, pk=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish('product_updated', serializer.data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # /api/products/<str:pk>  # delete object by pk [DELETE]
    def destroy(self, request, pk=None):
        product = Product.objects.get(id=pk)
        if product:
            product.delete()
            publish('product_deleted', pk)
            return Response(status=204)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'id': user.id,
        })

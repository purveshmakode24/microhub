from django.shortcuts import render
from .models import Product
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer
from rest_framework import status
from .producer import publish
from django.db import transaction
import random

# Create your views here.

class ProductViewSet(viewsets.ViewSet):

    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    """
    Added Transaction to handle data inconsistency due to publish failure.
    """
    @transaction.atomic
    def create(self, request):
        try:
            serializer = ProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print('test product created!')
            publish('product_created', serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            transaction.set_rollback(True)  # Rollback the transaction on exception
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, reqest, pk=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @transaction.atomic
    def update(self, request, pk=None):
        try:
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(instance=product, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            publish('product_updated', serializer.data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            transaction.set_rollback(True)  # Rollback the transaction on exception
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def destroy(self, request, pk=None):
        try:
            product = Product.objects.get(id=pk)
            product.delete()
            publish('product_deleted', pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            transaction.set_rollback(True)  # Rollback the transaction on exception
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserAPIView(APIView):
    def get(self, _):
        users = get_user_model().objects.all()
        user = random.choice(users)
        return Response({
            "id": user.id,
            "username": user.username
        })
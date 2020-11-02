from django.shortcuts import render
from rest_framework import generics, renderers
from .models import category, tenant, product, product_check_halal
from .serializer import CategorySerializer, TenantSerializer, ProductSerializer, HalalSerializer
from api.serializer import CartSerializer, ClientSerializer, PostCartSerializer, PromoSerializer, UclientSerializer
from api.models import order, promo, user
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.authtoken.models import Token
from .authentication import token_expire_handler, expires_in
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from api.authentication import ExpiringTokenAuthentication
# Create your views here.
class ApiAllCategory(generics.ListAPIView):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = CategorySerializer
    def get_queryset(self):
        queryset = category.objects.all()
        status = self.request.query_params.get('homepage', None)
        if status is not None:
            queryset = queryset.filter(show_homepage=status)
        return queryset


class ApiAllProduct(generics.ListAPIView):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = ProductSerializer
    def get_queryset(self):
        queryset = product.objects.all()
        pid = self.request.query_params.get('pid', None)
        if pid is not None:
            queryset = queryset.filter(id=pid)
        return queryset 


class ApiAllTenant(generics.ListAPIView):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = TenantSerializer
    def get_queryset(self):
        queryset = tenant.objects.all()
        tid = self.request.query_params.get('tid', None)
        if tid is not None:
            queryset = queryset.filter(id=tid)
        return queryset


class ApiCheckHalal(generics.ListAPIView):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = HalalSerializer
    def get_queryset(self):
        queryset = product_check_halal.objects.all()
        product = self.request.query_params.get('product', None)
        if product is not None:
            queryset = queryset.filter(product_id=product)
        return queryset


class ApiCart(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    def get_queryset(self):
        queryset = order.objects.all()
        oid = self.request.query_params.get('oid', None)
        if oid is not None:
            queryset = queryset.filter(order_id=oid)
        else:
            queryset = []
        return queryset

class ApiRegister(APIView):
    def post (self, request):
        # print(request.data)
        serializer = UclientSerializer(data=request.data)
        serializer.is_valid()
        u = user.objects.create(
            email = request.data['email'],
            full_name = request.data['full_name'],
            address = request.data['address'], 
            kecamatan = request.data['kecamatan'],
            kabupaten = request.data['kabupaten'],
            post_code = request.data['post_code'],
            phone = request.data['phone'],
            level = request.data['level']
            
        )
        u.set_password(request.data['password'])
        u.referal_id = request.data['referral']
        u.save()
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        a = serializer.data
        a.pop('password')
        print(a)
        return Response(a,status=status.HTTP_201_CREATED)

class ApiLogin(APIView):
    def post(self, request):
        print(request.data)
        # serializer = LoginSerializer(request.data)
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        client = authenticate(email=request.data['email'],password=request.data['password'])
        if not client:
            return Response({'detail': 'Invalid Credentials or activate account'}, status=status.HTTP_404_NOT_FOUND)
        client.is_login=True
        client.last_login = timezone.now()
        client.save()
        token, _ = Token.objects.get_or_create(user = client)
        is_expired, token = token_expire_handler(token)
        user_serialized = ClientSerializer(client) 
        # user_serialized.is_valid()
        return Response({
        'user': user_serialized.data, 
        'expires_in': expires_in(token),
        'token': token.key
    }, status=status.HTTP_200_OK)

class ApiReferral(generics.ListAPIView):
    serializer_class = ClientSerializer
    def get_queryset(self):
        email = self.kwargs['email']
        queryset = user.objects.all()
        queryset = queryset.filter(email=email)
        return queryset
        

class PostApiCart(APIView):
    authentication_classes = [SessionAuthentication, ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    def post(self, request):
        body_unicode = request.data
        body = json.dumps(body_unicode)
        serializer = PostCartSerializer(data=request.data)
        serializer.FillData(datas=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(body)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApiPromo(generics.ListAPIView):
    # renderer_classes = [renderers.JSONRenderer]
    serializer_class = PromoSerializer
    def get_queryset(self):
        queryset = promo.objects.all()
        return queryset

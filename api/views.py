from django.shortcuts import render
from django.views import View
from rest_framework import generics, renderers
from .models import category, tenant, product, product_check_halal
from .serializer import CategorySerializer, TenantSerializer, ProductSerializer, HalalSerializer
from api.serializer import BookmarkSerializer, CartSerializer, CartSerializerII, ClientSerializer, ControllBookmarkSerializer, FavouriteSerializer, PostCartSerializer, PostPayCod, PostPaymentStatus, PromoSerializer, UclientSerializer
from api.models import bookmark, order, order_detail, payment_status, promo, user
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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Count
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['$product_name']
    ordering_fields = ['product_price','product_date','point_demand','point_favourite']
    def get_queryset(self):
        queryset = product.objects.all()
        # self.serializer_class(queryset)
        pid = self.request.query_params.get('pid', None)
        cid = self.request.query_params.get('cid',None)
        if pid is not None:
            queryset = queryset.filter(id=pid)
        if cid is not None:
            queryset = queryset.filter(categories=cid)
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
    # authentication_classes = [SessionAuthentication, ExpiringTokenAuthentication]
    # permission_classes = [IsAuthenticated]
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
    # authentication_classes = [SessionAuthentication, ExpiringTokenAuthentication]
    # permission_classes = [IsAuthenticated]
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


class ApiFavourite(generics.ListAPIView):
# class ApiFavourite(APIView):
    serializer_class = FavouriteSerializer
    def get_queryset(self):
        is_desc = self.request.query_params.get('desc', None)
        if is_desc is not None:
            queryset = order_detail.objects.values('product_id').annotate(t=Count('product_id')).order_by('-t')
        else:
            queryset = order_detail.objects.values('product_id').annotate(t=Count('product_id')).order_by('t')
        return queryset
    # def get(self, request):
    #     data = order_detail.objects.all().values('product_id').annotate(t=Count('product_id')).order_by('t')
    #     return Response(data)


class ApiBookmark(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user_id']
    ordering_fields = ['bookmark_date']
    def get_queryset(self):
        queryset = bookmark.objects.all()
        return queryset


class APiAddBookmark(APIView):
    authentication_classes = [SessionAuthentication, ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer_class = ControllBookmarkSerializer(request.data)
        # if not serializer_class.is_valid():
        #     return Response(serializer_class.error_messages, status= status.HTTP_400_BAD_REQUEST)
        # serializer_class.save()
        p = product.objects.get(id=serializer_class.data['product_id'])
        point = p.point_favourite
        p.point_favourite = int(point) + 1
        p.save()
        return Response(serializer_class.data, status = status.HTTP_200_OK)


class ApiDeleteBookmark(APIView):
    authentication_classes = [SessionAuthentication, ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # idb = self.request.query_params.get('idb', None)
        idb = request.data['idb']
        try:
            b = bookmark.objects.get(id=idb)
        except :
            return Response(status=status.HTTP_404_NOT_FOUND)
        p = product.objects.get(id=b.product_id)
        point = p.point_favourite
        p.point_favourite = int(point) - 1
        p.save()
        if b is not None:
            b.delete()

            return Response({'status':'Delete Complete'},status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ApiPayCod(APIView):
    authentication_classes = [SessionAuthentication, ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = PostPayCod(request.data)
        order_ = order.objects.get(serializer.data['order_id'])
        order_.status='Done'
        order_.save()
        # 1602681574127
        details =order_detail.objects.filter(order_id=serializer.data['order_id'])
        for item in details:
            p = product.objects.get(id=item['product_id'])
            point = p.point_demand
            p.point_demand = int(point)+1
            p.save()
        return Response(status=status.HTTP_200_OK)
           
    # def get(self, request):
    #     order_details = order_detail.objects.filter(order_id='1602681574127')
    #     return Response(json.dumps(order_details))

class ApiTest(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__email']
    def get_queryset(self):
        queryset = order.objects.all()
        return queryset
    
class ApiUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = order.objects.all()
    serializer_class = CartSerializerII

@method_decorator(csrf_exempt, name='dispatch')
class NotificationPayment(View):
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        transaction_status = body['transaction_status']
        order_id = body['order_id']
        transaction_time = body['transaction_time']
        payment_type = body['payment_type']
        data = {
                    "order_id":order_id,
                    "transaction_time": transaction_time,
                    "transaction_status": transaction_status,
                    "payment_type": payment_type
            }
        if transaction_status=='settlement':
            orde = order.objects.get(order_id=order_id)
            orde.status="Payed"
            orde.save()
        elif transaction_status=='pending':
            orde = order.objects.get(order_id=order_id)
            orde.status="Pending"
            orde.save()
        else :
            orde = order.objects.get(order_id=order_id)
            orde.status="Failed"
            orde.save()
        pay = payment_status.objects.create(**data)
        pay.save()
        return HttpResponse('OK')

class ApiPostPayment(generics.ListCreateAPIView):
    serializer_class = PostPaymentStatus
    # queryset = payment_status.objects.all()
    def post(self, request):
        serializer = PostPaymentStatus(data=request.data)
        payment_status.objects.create(**request.data)
        return Response(status = status.HTTP_200_OK)
from django.shortcuts import render
#from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes,throttle_classes
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
from .throtters import TenCallsPerMinute
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User,Group

@api_view(['GET','POST'])
def itemlist(request):
    if request.method=='GET':
        items=MenuItem.objects.select_related('category').all()
        category_name=request.query_params.get('category')
        to_price=request.query_params.get('to_price')
        search=request.query_params.get('search')
        ordering=request.query_params.get('ordering')
        perpage=request.query_params.get('perpage',default=2)
        page=request.query_params.get('page',default=1)
        if category_name:
            items=items.filter(category__title=category_name)
        if to_price:
            items=items.filter(Price=to_price)
        if search:
            items=items.filter(Title__icontains=search)
        if ordering:
            #ordering_fields=ordering.split(",")
            items=items.order_by(ordering)
        paginator=Paginator(items,per_page=perpage)
        try:
            items=paginator.page(number=page)
        except EmptyPage:
                items=[]
          
        
        serializer_class=MenuItemSerializer(items,many=True)
        return Response(serializer_class.data)
    if request.method=='POST':
        serializer=MenuItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
          serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view()
def singleitem(request,id):
    item=get_object_or_404(MenuItem,pk=id)
    serializer=MenuItemSerializer(item,)
    return Response(serializer.data)
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({'message':"some secret message"})

@api_view()
@permission_classes([IsAuthenticated])
def managerview(request):
    if request.user.groups.filter(name='managers').exists():
        return Response({'message':"only manager secret message"})
    else:
        return Response({'message':"you are not authorized"},403)
    
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({'message':"some secret message"})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def throttle_check_auth(request):
    return Response({'message':"some secret message"})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_ten(request):
    return Response({'message':"some secret message"})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def managerview(request):
    username=request.data['username']
    if username:
        user=get_object_or_404(User,username=username)
        managers=Group.objects.get(name='managers')
        if request.method=='POST':
          managers.user_set.add(user)
        elif request.method=='DELETE':
            managers.user_set.remove(user)
        return  Response({"message":"ok"})
    return Response({"message":"error"},status=status.HTTP_400_BAD_REQUEST)






"""class Menuview(generics.ListCreateAPIView):
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer
class SingleItemView(generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer"""

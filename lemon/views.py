from django.shortcuts import render
#from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,EmptyPage
"""class Menuview(generics.ListCreateAPIView):
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer
class SingleItemView(generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer"""
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



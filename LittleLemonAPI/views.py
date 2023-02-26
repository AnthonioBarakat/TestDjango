from unicodedata import category
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework import generics, status
from traitlets import default
from .models import MenuItem

from rest_framework.decorators import api_view

from django.core.paginator import Paginator, EmptyPage

from .serializers import FunctionSerializer, MenuItemSerializer

from rest_framework.permissions import IsAuthenticated 
from rest_framework.decorators import permission_classes

# for throttling
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import AnonRateThrottle # for anonymous
from rest_framework.throttling import UserRateThrottle # for Authenticated user

from .throttles import TenCallsPerMinute

# Create your views here.

class MenuItemView(generics.ListCreateAPIView):
    # select_related() is used to perform single SQL instead of retrieve the title 
    # food from category pk for each menu item object
    queryset = MenuItem.objects.select_related('category').all() 
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
        if search:
            items = items.filter(title__contains=search)
        if ordering:
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)
        
        ##  Pagination ##
        # paginator = Paginator(items, per_page=perpage)
        # try:
        #     items= paginator.page(number=page)
        # except EmptyPage:
        #     items=[]

        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)
    if request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)

        # Get validated data
        ## data = serialized_item.validated_data ##

        # to save the data in the database =>
        serialized_item.save()
        # 'serialized_item.data' can be done if and only if saved in db
        return Response(serialized_item.data, status.HTTP_200_OK)

@api_view()
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = FunctionSerializer(item)
    return Response(serialized_item.data)


# for token
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    # To check the group of the user who make the request use =>
    # if request.user.groups.filter(name='Manager').exists():
    return Response({"Message": "Some secret message"})


# for throttling:
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"Message": "Successfull"})

@api_view()
@throttle_classes([UserRateThrottle])
@permission_classes([IsAuthenticated])
def throttle_check_user(request):
    return Response({"Message": "Successfull"})

@api_view()
@throttle_classes([TenCallsPerMinute])
def throttle_check_third(request):
    return Response({"Message": "Successfull"})
#### 




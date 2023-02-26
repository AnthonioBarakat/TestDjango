from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items/', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    
    path('menu-items-serializer/', views.menu_items),
    path('menu-items-serializer/<int:id>', views.single_item),
    
    path('secret/', views.secret),
    # generate token for a user (username and password be sent in post method)
    path('api-token-auth/', obtain_auth_token), 

    # for throttling
    path('throttle-check/', views.throttle_check),
    path('throttle-check-user/', views.throttle_check_user),
    path('throttle-check-third/', views.throttle_check_third),
]
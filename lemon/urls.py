from django.urls import path
from .views import itemlist,singleitem,secret,managerview,throttle_check,throttle_check_auth,throttle_check_ten,managerview
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns=[
    path('menu-items/',itemlist),
    path('menu-items/<int:id>',singleitem),
    path('secret/',secret),
    path('api-token-auth/',obtain_auth_token),
    path('manager/',managerview),
    path('throttle_check/',throttle_check),
    path('throttle_check_auth/',throttle_check_auth),
    path('throttle_check_ten/',throttle_check_ten),
    path('group/manager/users/',managerview),
]


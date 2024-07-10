from django.urls import path
from .views import itemlist,singleitem,secret,managerview,throttle_check
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns=[
    path('menu-items/',itemlist),
    path('menu-items/<int:id>',singleitem),
    path('secret/',secret),
    path('api-token-auth',obtain_auth_token),
    path('manager/',managerview),
    path('throttle_check/',throttle_check),
]

#t"token": "f4ecb22eab50eb3ddd6216207ecc2321f814790f"
#sm"token": "327995ed8321c9279ad118761735629a8060adc2"
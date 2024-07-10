from django.urls import path
from .views import itemlist,singleitem

urlpatterns=[
    path('menu-items/',itemlist),
    path('menu-items/<int:id>',singleitem),
]
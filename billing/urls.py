from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.billing_list,
        name="billing"
    ),

    

]
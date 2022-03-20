from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_data',views.user_data,name='user_data'),
    path('user/<str:user_id>/',views.get_details,name='get_details'),
]



from django.urls import path

from mainapp import views

# add_name='mainapp'
urlpatterns = [
    path('home/', views.homepage),
    path('userLogin/', views.userLogin),
    path('userSign/',views.userSign),
    path('upload/',views.upload),
    path('addUser/',views.addUser),
    path('verifycode/',views.verifycode),
    path('show/<int:blog_id>',views.show,name='show'),
    path('logout/',views.logout),
    path('wirteBlog/',views.wirteBlog),
    path('revert/',views.revert)

]


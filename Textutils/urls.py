from django.contrib import admin
from django.urls import path
from Textutils import views

admin.site.site_header = "Anupam website Admin"
admin.site.site_title = "Anupam website Admin Portal"
admin.site.index_title = "Welcome to Anupam website Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path("login/",views.loginUser,name='login'),
    path("logout/",views.logoutUser,name='logout'),
    path('analyze/',views.analyze, name='analyze'),
    path('about/',views.aboutus,name='aboutus'),
    path('contact/',views.contactus,name='contactus')
]
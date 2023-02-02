"""source URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from bacterial_genome_annotation import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'bacterial_genome_annotation'

# Admin url
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
]

# Base url
urlpatterns.extend([
    path('', views.home, name="home"),
    path('search/', views.Search, name="search"),
    path('alignement/', views.alignement, name="alignement"),
    path('annoter/', views.ANNOT, name='annoter'),
    path('AddGenome/', views.AddGenome, name="AddGenome"),
    path('AboutUs/', views.AboutUs, name="AboutUs"),
    path('contact/', views.contact, name="contact"),
])

# From a sequence
urlpatterns.extend([
    path('search/sequence/<str:id>', views.SequenceView, name='sequence'),
    path('Parser/<str:id>/', views.Parser, name="Parser"),
    path('annoter/<str:id>/', views.ANNOT, name="ANNOT"),
    path('search/genome/<str:id>', views.GenomeView, name='genome'),
])

# Registration and account management
urlpatterns.extend([
    path("login/", views.LoginView.as_view(), name='login'),
    path("logout/", views.LogoutView.as_view(), name='logout'),
    path("register/", views.SignUpView.as_view(), name="signup"),
    path('validate_email', views.validate_email, name='validate_email'),
    path('validate_password', views.validate_password, name='validate_password'),
    path('account/<str:id>', views.AccountView, name='account'),
    path('account/modification/', views.AccountModificationView, name='account_modification'),
    path('members/', views.MembersView, name='members'),
    path('account/add_friend/<str:id>', views.AddToFavorites, name='add_friend'),
    path('account/remove_friend/<str:id>', views.RemoveFromFavorites, name='remove_friend'),
])

urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

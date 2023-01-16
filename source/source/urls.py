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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name="home"),
    path('search/', views.Search, name="search"),
    path('search/sequence&id=<str:id>', views.SequenceView, name='sequence'),
    path('annoter/',views.annoter, name='annoter'),
    path('AddGenome/',views.AddGenome, name="AddGenome"),
    path('Parser&id=<str:id>/', views.Parser, name="Parser"),
    path('Account/',views.Account, name = 'Account'),
    #path('AddGenome.html/',views.LoginPage),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('validate_email', views.validate_email, name='validate_email'),
]

urlpatterns += static(settings.STATIC_URL,
 document_root=settings.STATIC_ROOT)

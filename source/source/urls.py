"""source URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
    # path('', views.home, name="home"),
    path('', views.Search, name="search"),
    path('Help/', views.help, name="Help"),
    path('annoter/', views.ANNOT, name='annoter'),
    path('', views.home, name="home"),
    path('alignment/', views.alignment, name="alignment"),
    path('AddGenome/', views.AddGenome, name="AddGenome"),
    path('AboutUs/', views.AboutUs, name="AboutUs"),
    path('contact/', views.contact, name="contact"),
    path('FAQ/', views.FAQ, name='FAQ'),
    ])

# From a sequence
urlpatterns.extend([
    path('alignment/<str:id>/', views.alignment, name="alignment"),
    path('annoter/<str:id>/', views.ANNOT, name="ANNOT"),
    path('sequence/<str:id>/', views.SequenceView, name='sequence'),
    path('sequence/<str:id>/Parser/', views.Parser, name="Parser"),
    path('sequence/<str:id>/annoter/', views.ANNOT, name="annotate"),
    path('annotation/<str:id>/valid/', views.Valid_Annotation, name="valid_annotation"),
    path('annotation/<str:id>/delete/', views.Delete_Annotation, name="delete_annotation"),
    path('sequence/<str:id>/assign/', views.Assign, name='assign'),
    path('genome/<str:id>', views.GenomeView, name='genome'),
    ])

# Registration and account management
urlpatterns.extend([
    path("login/", views.LoginView.as_view(), name='login'),
    path("logout/", views.LogoutView.as_view(), name='logout'),
    path("register/", views.SignUpView.as_view(), name="signup"),
    path('validate_email', views.validate_email, name='validate_email'),
    path('validate_password', views.validate_password, name='validate_password'),
    path('account/<str:id>', views.AccountView, name='account'),
    path('account/<str:id>/add_friend/', views.AddToFavorites, name='add_friend'),
    path('account/<str:id>/remove_friend/', views.RemoveFromFavorites, name='remove_friend'),
    path('account/<str:id>/promote_to_annotator/', views.PromoteToAnnotator, name='promote_to_annotator'),
    path('account/<str:id>/promote_to_validator/', views.PromoteToValidator, name='promote_to_validator'),
    path('account/<str:id>/promote_to_admin/', views.PromoteToAdmin, name='promote_to_admin'),
    path('account/<str:id>/downgrade/', views.Downgrade, name='downgrade'),
    path('members/', views.MembersView, name='members'),
    ])

urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

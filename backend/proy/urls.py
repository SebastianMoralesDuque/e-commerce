from django.contrib import admin
from django.urls import path, include
from app import views
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from graphene_file_upload.django import FileUploadGraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
    path('guardar-imagen/', csrf_exempt(views.guardar_imagen)),
    path('productos/<path:path>/', views.productos_fotos_view),
    
]

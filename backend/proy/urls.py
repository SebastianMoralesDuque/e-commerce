from django.contrib import admin
from django.urls import path
from app import views
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/data/', views.api_data_view),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
]

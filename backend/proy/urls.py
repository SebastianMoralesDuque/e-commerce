from django.contrib import admin
from django.urls import path
from app import views
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/data/', views.api_data_view),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]

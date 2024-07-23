from home.views import index, person, login , PersonAPI, PeopleViewSet,RegisterApi,LoginAPI,ImageModelAPI,MyImageViewSet
# MultImageModelAPI
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'people', PeopleViewSet, basename='people')
urlpatterns = router.urls 

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterApi.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/', LoginAPI.as_view()),
    path('images/', ImageModelAPI.as_view({'get': 'list', 'post': 'create'})),
    path('index/', index),
    path("person/", person),
    path("login/", login),
    path("persons/", PersonAPI.as_view()),
    path("myimage/", MyImageViewSet.as_view({'get': 'list', 'post': 'create', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('myimage/<int:pk>/image/<int:image_pk>/', MyImageViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy' }), name='myimage-partial-update')
    
]

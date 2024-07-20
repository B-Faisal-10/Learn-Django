from rest_framework.decorators import api_view
from rest_framework.response import Response

from home.models import Person, ImageModel, MyImage,Image
from home.serializers import PeopleSerializer, LoginSerializer, RegisterSerializer, ImageModelSerializer,ImageSerializer,MyImageSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

class MyImageViewSet(viewsets.ModelViewSet):
    queryset = MyImage.objects.all()
    serializer_class = MyImageSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        image_pk = kwargs.get('image_pk')
        
        try:
            image_instance = Image.objects.get(pk=image_pk, my_image=instance)
        except Image.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ImageSerializer(image_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        image_pk = kwargs.get('image_pk')
        
        try:
            image_instance = Image.objects.get(pk=image_pk, my_image=instance)
        except Image.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
        
        image_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageModelAPI(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageModelSerializer

class LoginAPI(APIView):
    
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)
        if not serializer.is_valid():
            return Response ({
                'status': False,
                'message': serializer.errors
                },
                status.HTTP_400_BAD_REQUEST
            )
        print(serializer.data)
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        print(user)
        if not user:
            return Response ({
                'status': False,
                'message': 'Invalid Credentials'
                },
                status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)
        # print(token)
        return Response({'status': True, 'message': 'user login', 'refresh': str(refresh),
        'access': str(refresh.access_token)}, status.HTTP_201_CREATED)


class RegisterApi(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response ({
                'status': False,
                'message': serializer.errors
                },
                status.HTTP_400_BAD_REQUEST
            )
        serializer.save()

        return Response({'status': True, 'message': 'user created'}, status.HTTP_201_CREATED)




@api_view(['GET','POST'])
def index(request):
    if request.method == 'GET':
        json_response = {
            'name': 'Scaler',
            'courses': ['C++', 'Python'],
            'method': 'GET'
        }
    else:
        data = request.data
        print(data)
        json_response = {
            'name': 'Scaler',
            'courses': ['C++', 'Python'],
            'method': 'POST'
        }

    return Response(json_response)


@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)

    if serializer.is_valid():
        data = serializer.data
        print(data)
        return Response({'message': 'success'})

    return Response(serializer.errors)


from django.core.paginator import Paginator

class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
   
    def get(self, request):
        try:
            print(request.user)
            obj = Person.objects.all()
            page = request.GET.get('page', 1)
            page_size = 3
            paginator = Paginator(obj, page_size)
            serializer = PeopleSerializer(paginator.page(page), many = True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'status': False,
                'message': 'invalid page'
            })

    def post(self, request):
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
        

    def put(self, request):
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj, data = data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

        
    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id= data['id'])
        obj.delete()
        return Response({'message': 'person deleted'})
        





@api_view(['GET','POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == 'GET':
        obj = Person.objects.filter(color__isnull=False)
        serializer = PeopleSerializer(obj, many = True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == 'PUT':
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj, data = data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    else:
        data = request.data
        obj = Person.objects.get(id= data['id'])
        obj.delete()
        return Response({'message': 'person deleted'})





class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)

        serializer = PeopleSerializer(queryset, many=True)
        return Response({'status': 200, 'data': serializer.data},status=status.HTTP_204_NO_CONTENT)



    @action(detail=True, methods=['post'])
    def send_mail_to_person(self, request, pk):
        obj = Person.objects.get(pk = pk)
        serializer = PeopleSerializer(obj)
        
        return Response({
            'status' : True,
            'message' : 'email sent succesfully',
            'data' : serializer.data
        })
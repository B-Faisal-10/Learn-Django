from rest_framework import serializers
from .models import Person, Color, ImageModel,MyImage,Image
from django.contrib.auth.models import User


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=False)

    class Meta:
        model = Image
        fields = "__all__"

class MyImageSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=True, read_only=True)
    uploaded_img = serializers.ListField(
        child=serializers.ImageField(max_length=100, allow_empty_file=False), write_only=True )
   

    class Meta:
        model = MyImage
        fields = ['id', 'title', 'image', 'uploaded_img']

    def create(self, validated_data):
            uploaded_img = validated_data.pop("uploaded_img",[])
            my_image = MyImage.objects.create(**validated_data)
            for image_data in uploaded_img:
                Image.objects.create(my_image=my_image, image=image_data)

            return my_image

class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = '__all__'

        def get_photo_url(self, obj):
            request = self.context.get('request')
            photo_url = obj.fingerprint.url
            return request.build_absolute_url(photo_url)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):

        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError('username is taken')

        if data['email']:
            if User.objects.filter(username = data['email']).exists():
                raise serializers.ValidationError('email is taken')
        return data

    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'], email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
        print(validated_data)



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id','color_name']


class PeopleSerializer(serializers.ModelSerializer):
   
    color_info = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = '__all__'
        # depth = 1

    def get_color_info(self, obj):
        if obj.color:
            color_obj = Color.objects.get(id = obj.color.id)
            return {'color_name': color_obj.color_name, 'hex_code': '#000'}
        return None

    def validate(self, data):

        special_characters = "!@#$%^&*()_+?=,<>/"
        if any(c in special_characters for c in data['name']):
            raise serializers.ValidationError('name cannot contain special chars')
        # if data['age'] < 18:
        #     raise serializers.ValidationError('age should be greater than 18')
        
        return data
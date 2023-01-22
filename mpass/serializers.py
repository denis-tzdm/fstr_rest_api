from rest_framework import serializers

from .models import Coords, MPassUser, AddedMPass, Image


class CoordsSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(source='lat')
    longitude = serializers.FloatField(source='lon')

    class Meta:
        model = Coords
        fields = [
            'latitude',
            'longitude',
            'height',
        ]


class UserSerializer(serializers.ModelSerializer):
    fam = serializers.CharField(source='name_sur', label='Surname', allow_blank=True)
    otc = serializers.CharField(source='name_pat', label='Patronymic', allow_blank=True)

    class Meta:
        model = MPassUser
        fields = [
            'email',
            'name',
            'fam',
            'otc',
            'phone',
        ]
        extra_kwargs = {
            'email': {'validators': []},
        }


class LevelSerializer(serializers.Serializer):
    winter = serializers.CharField(allow_blank=True, max_length=2)
    spring = serializers.CharField(allow_blank=True, max_length=2)
    summer = serializers.CharField(allow_blank=True, max_length=2)
    autumn = serializers.CharField(allow_blank=True, max_length=2)


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = [
            'title',
            'data',
        ]


class MPassSerializer(serializers.ModelSerializer):
    connect = serializers.CharField(source='connects', label='Connects', allow_blank=True)
    coords = CoordsSerializer()
    user = UserSerializer()
    level = LevelSerializer(source='get_levels')
    images = ImageSerializer(source='mpass_images', many=True)

    class Meta:
        model = AddedMPass
        fields = [
            'beauty_title',
            'title',
            'other_titles',
            'connect',
            'add_time',
            'coords',
            'user',
            'level',
            'images',
        ]

    def create(self, validated_data):
        coords = validated_data.pop('coords')
        user = validated_data.pop('user')
        levels = validated_data.pop('get_levels')
        images = validated_data.pop('mpass_images')
        user_instance = MPassUser.objects.filter(email=user['email']).first()
        if not user_instance:
            user_instance = MPassUser.objects.create(**user)
        coords_instance, created = Coords.objects.get_or_create(**coords)
        pass_instance = AddedMPass.objects.create(
            user=user_instance,
            coords=coords_instance,
            **validated_data
        )
        pass_instance.set_levels(**levels)
        for image in images:
            Image.objects.create(mpass=pass_instance, **image)
        return pass_instance

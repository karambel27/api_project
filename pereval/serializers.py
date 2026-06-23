from rest_framework import serializers
from .models import User, Coords, Level, PerevalAdded, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone', ]


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height', ]


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring', ]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['data', 'title', ]


class PerevalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = PerevalAdded
        fields = ['id', 'beauty_title', 'title', 'other_titles',
                  'connect', 'add_time', 'user', 'coords', 'level',
                  'images', 'status',
                  ]

        read_only_fields = ['id', 'status',]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images')

        user, created = User.objects.get_or_create(
            email=user_data['email'],
            defaults={
                'fam': user_data['fam'],
                'name': user_data['name'],
                'otc': user_data.get('otc', ''),
                'phone': user_data['phone'],
            }
        )

        coords = Coords.objects.create(**coords_data)
        level = Level.objects.create(**level_data)

        pereval = PerevalAdded.objects.create( user=user, coords=coords, level=level, status='new', **validated_data)

        for image_data in images_data:
            Image.objects.create(
                pereval=pereval,
                **image_data
            )

        return pereval

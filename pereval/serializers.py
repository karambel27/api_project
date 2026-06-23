from rest_framework import serializers

from .models import User, Coords, Level, PerevalAdded, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone']


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['data', 'title']


class PerevalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = PerevalAdded
        fields = [
            'id',
            'beauty_title',
            'title',
            'other_titles',
            'connect',
            'add_time',
            'user',
            'coords',
            'level',
            'images',
            'status',
        ]
        read_only_fields = ['id', 'status']

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

        pereval = PerevalAdded.objects.create(
            user=user,
            coords=coords,
            level=level,
            status='new',
            **validated_data
        )

        for image_data in images_data:
            Image.objects.create(
                pereval=pereval,
                **image_data
            )

        return pereval

    def update(self, instance, validated_data):
        validated_data.pop('user', None)

        coords_data = validated_data.pop('coords', None)
        level_data = validated_data.pop('level', None)
        images_data = validated_data.pop('images', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if coords_data:
            for attr, value in coords_data.items():
                setattr(instance.coords, attr, value)
            instance.coords.save()

        if level_data:
            for attr, value in level_data.items():
                setattr(instance.level, attr, value)
            instance.level.save()

        if images_data is not None:
            instance.images.all().delete()

            for image_data in images_data:
                Image.objects.create(
                    pereval=instance,
                    **image_data
                )

        instance.save()

        return instance
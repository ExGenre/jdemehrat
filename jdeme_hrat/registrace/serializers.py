from rest_framework import serializers
from .models import Event, Participation, Comment, UserProfile, CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'profile_pic', 'id']  # Zde uvedte pole, která chcete zobrazit

class ParticipationSerializer(serializers.ModelSerializer):
    uzivatel = UserSerializer(read_only=True)

    class Meta:
        model = Participation
        fields = '__all__'
        read_only_fields = ('uzivatel',)

class EventSerializer(serializers.ModelSerializer):
    vytvoreno_uzivatelem = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    ucastnici = ParticipationSerializer(source='participation_set', many=True, read_only=True)
    class Meta:
        model = Event
        fields = '__all__'  # nebo ['nazev', 'popis', 'hra', 'datum_konani', 'misto', 'vytvoril']


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='uzivatel.username', read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
from dataclasses import fields
from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    # This owner object will return owner from profile serializer, else it will only show the id of the owner
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    # for the child class of project 
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    # we need to use get_ for our methods 
    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
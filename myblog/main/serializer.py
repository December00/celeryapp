from rest_framework import serializers
from .models import Blog

class BlogModel:
    def __init__(self,title,content):
        self.title = title
        self.content = content


class BlogSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    date = serializers.DateTimeField()
    content = serializers.CharField()
    likes = serializers.IntegerField(default=0, read_only=True)

    def create(self, validated_data):
        validated_data['likes'] = validated_data.get('likes', 0)
        return Blog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.date = validated_data.get("date", instance.date)
        instance.content = validated_data.get("content", instance.content)
        instance.likes = validated_data.get("likes", instance.likes)

        instance.save()
        return instance

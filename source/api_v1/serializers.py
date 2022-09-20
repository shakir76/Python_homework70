from rest_framework import serializers

from webapp.models import Article


class ArticleModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

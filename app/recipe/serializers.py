from rest_framework import serializers
from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe Serializer"""
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']

    """Create Recipe"""

    def create(self, validated_data):
        print(validated_data)
        recipe = Recipe.objects.create(**validated_data)
        return recipe


class RecipeDetailSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article, Category

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur existe déjà.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    #pour les articles (afficher les articles, filter, detail) et create une article

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'content', 'author', 'category',
            'image', 'created_at', 'updated_at', 'is_published', 'views'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at', 'views', 'slug']

    def validate(self, data):
        if not data.get('title'):
            raise serializers.ValidationError({"title": "Le titre est obligatoire."})
        return data

    def create(self, validated_data):
        # L’auteur est automatiquement l’utilisateur connecté
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
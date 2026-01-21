from django.db.models.query_utils import Q
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from .models import Article, Category
from .serializers import ArticleSerializer, RegisterSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly

# pour gerer les Inscription
class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "detail": "Utilisateur créé avec succès",
            "username": user.username
        }, status=201)

#vue categorie pour afficher les categories dependenment des articles.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

    http_method_names = ['get', 'head', 'options']

# Articles crud
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
    page_size = 10
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category__slug']
    search_fields = ['title', 'content']
    lookup_field = 'slug'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Article.objects.filter(Q(is_published=True)|Q(author=self.request.user)).distinct().order_by('-created_at')
        return Article.objects.filter(is_published=True).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return super().get_permissions()
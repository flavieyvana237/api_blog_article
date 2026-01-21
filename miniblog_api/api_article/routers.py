# api_article/routers.py

from rest_framework import routers
from .views import ArticleViewSet, RegisterViewSet, CategoryViewSet
router = routers.DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = router.urls
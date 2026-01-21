from django.contrib import admin
from .models import Category, Article

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'created_at')
    list_filter = ('is_published', 'category')  # ← on garde le filtre sur category (ForeignKey)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    # Plus de filter_horizontal (car on a une seule catégorie maintenant)



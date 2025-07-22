
from django.contrib import admin
from .models import Category, Watch, HomeBanner, PromotionalText, Slider, FooterSection, FooterLink

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_number', 'category', 'price', 'availability', 'is_featured', 'created_at']
    list_filter = ['category', 'availability', 'is_featured', 'created_at']
    search_fields = ['name', 'model_number', 'description']
    prepopulated_fields = {'slug': ('name', 'model_number')}
    list_editable = ['is_featured', 'availability']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'model_number', 'category', 'description', 'slug')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'availability', 'is_featured')
        }),
        ('Images', {
            'fields': ('image', 'image_2', 'image_3')
        }),
        ('Features', {
            'fields': ('features',)
        })
    )

@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active', 'order']
    search_fields = ['title', 'subtitle']

@admin.register(PromotionalText)
class PromotionalTextAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active']
    search_fields = ['title', 'content']

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active', 'order']
    search_fields = ['title', 'subtitle', 'description']

class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1

@admin.register(FooterSection)
class FooterSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active', 'order']
    search_fields = ['title', 'content']
    inlines = [FooterLinkInline]

@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'is_active', 'order']
    list_filter = ['section', 'is_active']
    list_editable = ['is_active', 'order']
    search_fields = ['title', 'url']

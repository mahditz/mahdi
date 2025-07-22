
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Watch, HomeBanner, PromotionalText, Slider, FooterSection

def home(request):
    categories = Category.objects.all()[:4]  # Show first 4 categories
    featured_watches = Watch.objects.filter(is_featured=True)[:6]
    banners = HomeBanner.objects.filter(is_active=True)
    promotional_texts = PromotionalText.objects.filter(is_active=True)
    sliders = Slider.objects.filter(is_active=True)
    footer_sections = FooterSection.objects.filter(is_active=True)
    
    context = {
        'categories': categories,
        'featured_watches': featured_watches,
        'banners': banners,
        'promotional_texts': promotional_texts,
        'sliders': sliders,
        'footer_sections': footer_sections,
    }
    return render(request, 'watches/home.html', context)

def watch_list(request):
    category_slug = request.GET.get('category')
    watches = Watch.objects.all()
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        watches = watches.filter(category=category)
        
    paginator = Paginator(watches, 12)  # Show 12 watches per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    footer_sections = FooterSection.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'footer_sections': footer_sections,
    }
    return render(request, 'watches/watch_list.html', context)

def watch_detail(request, slug):
    watch = get_object_or_404(Watch, slug=slug)
    related_watches = Watch.objects.filter(category=watch.category).exclude(id=watch.id)[:4]
    footer_sections = FooterSection.objects.filter(is_active=True)
    
    context = {
        'watch': watch,
        'related_watches': related_watches,
        'footer_sections': footer_sections,
    }
    return render(request, 'watches/watch_detail.html', context)

def category_list(request):
    categories = Category.objects.all()
    footer_sections = FooterSection.objects.filter(is_active=True)
    
    context = {
        'categories': categories,
        'footer_sections': footer_sections,
    }
    return render(request, 'watches/category_list.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    watches = Watch.objects.filter(category=category)
    
    paginator = Paginator(watches, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    footer_sections = FooterSection.objects.filter(is_active=True)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'footer_sections': footer_sections,
    }
    return render(request, 'watches/category_detail.html', context)

def contact(request):
    footer_sections = FooterSection.objects.filter(is_active=True)
    
    context = {
        'footer_sections': footer_sections,
    }
    return render(request, 'watches/contact.html', context)

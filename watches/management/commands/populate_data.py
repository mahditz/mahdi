
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from watches.models import Category, Watch, HomeBanner, PromotionalText
import requests
from io import BytesIO


class Command(BaseCommand):
    help = 'Populate database with sample watches, categories, and banners'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))
        
        # Create categories
        categories_data = [
            {
                'name': 'Luxury Watches',
                'description': 'Premium timepieces crafted with the finest materials and exceptional craftsmanship.',
                'image_url': 'https://images.unsplash.com/photo-1523170335258-f5c6c6bd6eaf?w=800&h=600&fit=crop'
            },
            {
                'name': 'Sport Watches',
                'description': 'Durable and functional watches designed for active lifestyles and outdoor adventures.',
                'image_url': 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=800&h=600&fit=crop'
            },
            {
                'name': 'Smart Watches',
                'description': 'Advanced wearable technology combining traditional timekeeping with modern smart features.',
                'image_url': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=800&h=600&fit=crop'
            },
            {
                'name': 'Classic Watches',
                'description': 'Timeless designs that never go out of style, perfect for any occasion.',
                'image_url': 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=800&h=600&fit=crop'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
            
            # Download and save category image
            if not category.image and cat_data.get('image_url'):
                try:
                    response = requests.get(cat_data['image_url'])
                    if response.status_code == 200:
                        image_content = ContentFile(response.content)
                        category.image.save(f'{category.slug}.jpg', image_content, save=True)
                        self.stdout.write(f'Added image for category: {category.name}')
                except Exception as e:
                    self.stdout.write(f'Could not download image for {category.name}: {e}')

        # Create sample watches
        watches_data = [
            {
                'name': 'Royal Heritage',
                'model_number': 'RH-001',
                'category': 'Luxury Watches',
                'price': 2499.99,
                'description': 'An exquisite timepiece featuring 18k gold plating, Swiss movement, and diamond hour markers. This watch represents the pinnacle of luxury craftsmanship.',
                'features': 'Swiss Movement, 18k Gold Plating, Diamond Hour Markers, Sapphire Crystal, Water Resistant 100m',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1547996160-81dfa63595aa?w=800&h=800&fit=crop'
            },
            {
                'name': 'Ocean Explorer',
                'model_number': 'OE-002',
                'category': 'Sport Watches',
                'price': 899.99,
                'description': 'Built for adventure, this diving watch features professional-grade water resistance and a unidirectional rotating bezel.',
                'features': 'Water Resistant 300m, Unidirectional Bezel, Luminous Hands, Stainless Steel, Anti-Magnetic',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=800&h=800&fit=crop'
            },
            {
                'name': 'Tech Pro Max',
                'model_number': 'TPM-003',
                'category': 'Smart Watches',
                'price': 549.99,
                'description': 'The ultimate smart watch with health monitoring, GPS tracking, and seamless smartphone integration.',
                'features': 'Heart Rate Monitor, GPS, Bluetooth 5.0, 7-Day Battery, Fitness Tracking, Voice Assistant',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=800&h=800&fit=crop'
            },
            {
                'name': 'Vintage Classic',
                'model_number': 'VC-004',
                'category': 'Classic Watches',
                'price': 399.99,
                'description': 'A timeless design that captures the elegance of vintage watchmaking with modern reliability.',
                'features': 'Automatic Movement, Leather Strap, Date Display, Anti-Reflective Crystal, 50m Water Resistant',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1509048191080-d2e2678e4f4e?w=800&h=800&fit=crop'
            },
            {
                'name': 'Elite Chronograph',
                'model_number': 'EC-005',
                'category': 'Luxury Watches',
                'price': 1899.99,
                'description': 'Precision timing meets luxury in this sophisticated chronograph with multiple sub-dials.',
                'features': 'Chronograph Function, Tachymeter, Swiss Quartz, Stainless Steel Bracelet, Scratch Resistant',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1523170335258-f5c6c6bd6eaf?w=800&h=800&fit=crop'
            },
            {
                'name': 'Urban Runner',
                'model_number': 'UR-006',
                'category': 'Sport Watches',
                'price': 299.99,
                'description': 'Designed for urban athletes, featuring shock resistance and multi-sport tracking capabilities.',
                'features': 'Shock Resistant, Stopwatch, Alarm, Backlight, Rubber Strap, Water Resistant 200m',
                'availability': 'pre_order',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=800&h=800&fit=crop'
            }
        ]

        for watch_data in watches_data:
            category = categories[watch_data['category']]
            watch, created = Watch.objects.get_or_create(
                model_number=watch_data['model_number'],
                defaults={
                    'name': watch_data['name'],
                    'category': category,
                    'price': watch_data['price'],
                    'description': watch_data['description'],
                    'features': watch_data['features'],
                    'is_featured': watch_data['is_featured'],
                    'availability': watch_data.get('availability', 'in_stock')
                }
            )
            
            if created:
                self.stdout.write(f'Created watch: {watch.name}')
                
                # Download and save watch image
                if watch_data.get('image_url'):
                    try:
                        response = requests.get(watch_data['image_url'])
                        if response.status_code == 200:
                            image_content = ContentFile(response.content)
                            watch.image.save(f'{watch.slug}.jpg', image_content, save=True)
                            self.stdout.write(f'Added image for watch: {watch.name}')
                    except Exception as e:
                        self.stdout.write(f'Could not download image for {watch.name}: {e}')

        # Create home banners
        banners_data = [
            {
                'title': 'Luxury Redefined',
                'subtitle': 'Discover Timeless Elegance',
                'description': 'Experience the finest collection of luxury watches crafted for those who appreciate perfection.',
                'link_text': 'Shop Luxury',
                'link_url': '/category/luxury-watches/',
                'image_url': 'https://images.unsplash.com/photo-1547996160-81dfa63595aa?w=1920&h=1080&fit=crop',
                'order': 1
            },
            {
                'title': 'Adventure Awaits',
                'subtitle': 'Built for Extreme Conditions',
                'description': 'Professional-grade sport watches designed to withstand any challenge nature throws at you.',
                'link_text': 'Explore Sports',
                'link_url': '/category/sport-watches/',
                'image_url': 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=1920&h=1080&fit=crop',
                'order': 2
            },
            {
                'title': 'Smart Innovation',
                'subtitle': 'Technology Meets Style',
                'description': 'Advanced smart watches that seamlessly blend cutting-edge technology with elegant design.',
                'link_text': 'Go Smart',
                'link_url': '/category/smart-watches/',
                'image_url': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=1920&h=1080&fit=crop',
                'order': 3
            }
        ]

        for banner_data in banners_data:
            banner, created = HomeBanner.objects.get_or_create(
                title=banner_data['title'],
                defaults={
                    'subtitle': banner_data['subtitle'],
                    'description': banner_data['description'],
                    'link_text': banner_data['link_text'],
                    'link_url': banner_data['link_url'],
                    'order': banner_data['order'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'Created banner: {banner.title}')
                
                # Download and save banner image
                if banner_data.get('image_url'):
                    try:
                        response = requests.get(banner_data['image_url'])
                        if response.status_code == 200:
                            image_content = ContentFile(response.content)
                            banner.image.save(f'banner_{banner.id}.jpg', image_content, save=True)
                            self.stdout.write(f'Added image for banner: {banner.title}')
                    except Exception as e:
                        self.stdout.write(f'Could not download image for {banner.title}: {e}')

        # Create promotional texts
        promo_data = [
            {
                'title': 'Craftsmanship Excellence',
                'content': 'Each timepiece in our collection is meticulously crafted by master watchmakers, ensuring exceptional quality and precision that lasts for generations.'
            },
            {
                'title': 'Lifetime Warranty',
                'content': 'We stand behind our products with a comprehensive lifetime warranty, providing you with peace of mind and confidence in your investment.'
            }
        ]

        for promo in promo_data:
            promotional_text, created = PromotionalText.objects.get_or_create(
                title=promo['title'],
                defaults={
                    'content': promo['content'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'Created promotional text: {promotional_text.title}')

        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Created {Category.objects.count()} categories'))
        self.stdout.write(self.style.SUCCESS(f'Created {Watch.objects.count()} watches'))
        self.stdout.write(self.style.SUCCESS(f'Created {HomeBanner.objects.count()} banners'))
        self.stdout.write(self.style.SUCCESS(f'Created {PromotionalText.objects.count()} promotional texts'))

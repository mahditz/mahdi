
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from watches.models import Slider, FooterSection, FooterLink

class Command(BaseCommand):
    help = 'Populate initial slider and footer data'

    def handle(self, *args, **options):
        # Create slider data
        sliders_data = [
            {
                'title': 'Luxury Redefined',
                'subtitle': 'Discover Timeless Elegance',
                'description': 'Experience the finest collection of luxury watches crafted for those who appreciate perfection.',
                'button_text': 'Shop Luxury',
                'button_url': '/watches/',
                'order': 1,
                'image_url': 'https://images.unsplash.com/photo-1547996160-81dfa63595aa?w=1920&h=1080&fit=crop'
            },
            {
                'title': 'Adventure Awaits',
                'subtitle': 'Built for Extreme Conditions',
                'description': 'Professional-grade sport watches designed to withstand any challenge nature throws at you.',
                'button_text': 'Explore Sports',
                'button_url': '/watches/',
                'order': 2,
                'image_url': 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=1920&h=1080&fit=crop'
            },
            {
                'title': 'Smart Innovation',
                'subtitle': 'Technology Meets Style',
                'description': 'Advanced smart watches that seamlessly blend cutting-edge technology with elegant design.',
                'button_text': 'Go Smart',
                'button_url': '/watches/',
                'order': 3,
                'image_url': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=1920&h=1080&fit=crop'
            }
        ]

        for slider_data in sliders_data:
            slider, created = Slider.objects.get_or_create(
                title=slider_data['title'],
                defaults={
                    'subtitle': slider_data['subtitle'],
                    'description': slider_data['description'],
                    'button_text': slider_data['button_text'],
                    'button_url': slider_data['button_url'],
                    'order': slider_data['order'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'Created slider: {slider.title}')
                
                # Download and save slider image
                if slider_data.get('image_url'):
                    try:
                        response = requests.get(slider_data['image_url'])
                        if response.status_code == 200:
                            image_content = ContentFile(response.content)
                            slider.image.save(f'slider_{slider.id}.jpg', image_content, save=True)
                            self.stdout.write(f'Added image for slider: {slider.title}')
                    except Exception as e:
                        self.stdout.write(f'Could not download image for {slider.title}: {e}')

        # Create footer sections
        footer_sections_data = [
            {
                'title': 'About LuxTime',
                'content': 'LuxTime is your premier destination for luxury timepieces. We curate the finest watches from renowned brands worldwide, offering exceptional quality and timeless elegance.',
                'order': 1
            },
            {
                'title': 'Customer Service',
                'content': 'We are committed to providing exceptional customer service. Contact us for any questions about our products or services.',
                'order': 2
            },
            {
                'title': 'Quick Links',
                'content': '',
                'order': 3
            },
            {
                'title': 'Contact Info',
                'content': '<p>📧 info@luxtime.com</p><p>📞 +1 (555) 123-4567</p><p>📍 123 Luxury Lane, Premium City, PC 12345</p>',
                'order': 4
            }
        ]

        for section_data in footer_sections_data:
            section, created = FooterSection.objects.get_or_create(
                title=section_data['title'],
                defaults={
                    'content': section_data['content'],
                    'order': section_data['order'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'Created footer section: {section.title}')

        # Create footer links for Quick Links section
        quick_links_section = FooterSection.objects.get(title='Quick Links')
        footer_links_data = [
            {'title': 'All Watches', 'url': '/watches/', 'order': 1},
            {'title': 'Categories', 'url': '/categories/', 'order': 2},
            {'title': 'Contact Us', 'url': '/contact/', 'order': 3},
            {'title': 'Privacy Policy', 'url': '#', 'order': 4},
            {'title': 'Terms of Service', 'url': '#', 'order': 5}
        ]

        for link_data in footer_links_data:
            link, created = FooterLink.objects.get_or_create(
                title=link_data['title'],
                section=quick_links_section,
                defaults={
                    'url': link_data['url'],
                    'order': link_data['order'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'Created footer link: {link.title}')

        self.stdout.write(self.style.SUCCESS('Successfully populated slider and footer data!'))

from django.db import models
from django.shortcuts import render 

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from our_stories_specific.models import OurStoriesSpecific, General_Stories
from related_projects.models import Related_Projects, General_Projects
from our_partner_areas.models import OurPartnerAreas, PartnerArea, PartnerAreaOrderable


class HomePage(Page):
    template = 'home/home_page.html'

    max_count = 1

    # Carousel of Images
    carousel = StreamField([
        ('Images', ImageChooserBlock(null=True)),
    ], null=True)

    # Our Projects Header
    header = models.TextField(null=True)

    # Our Projects Description
    desc = StreamField([
        ('Description', blocks.RichTextBlock(null = True)),
    ], null=True)

    # Mission and Vision Descriptions
    mission_desc = StreamField([
        ('MissionDescription', blocks.RichTextBlock(null = True))
    ], null=True)
    vision_desc = StreamField([
        ('VisionDescription', blocks.RichTextBlock(null = True))
    ], null=True)

    search_fields = Page.search_fields + [
    ]

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        StreamFieldPanel('desc'),
        StreamFieldPanel('carousel'),
        StreamFieldPanel('mission_desc'),
        StreamFieldPanel('vision_desc'),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['projects'] = Related_Projects.objects.live().order_by('-first_published_at')[:4]
        context['get_projects'] = General_Projects.objects.first()
        context['stories'] = OurStoriesSpecific.objects.live().order_by('-first_published_at')[:3]
        context['get_stories'] = General_Stories.objects.first()
        context['partner_areas'] = PartnerArea.objects.all()[:4]
        context['get_partners'] = OurPartnerAreas.objects.first()

        return context

        #sets slug to home
    def full_clean(self, *args, **kwargs):
        super(HomePage, self).full_clean(*args, **kwargs)

        if not self.slug.startswith('home'):
            self.slug = 'home'

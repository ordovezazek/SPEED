from __future__ import unicode_literals

from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from modelcluster.fields import ParentalManyToManyField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)


from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Collection, Page, Orderable
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from our_stories_specific.models import OurStoriesSpecific
from wagtail.search.models import Query

class General_Projects(Page):
    template = 'projects/projects.html'

    max_count = 1

    background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    desc = StreamField([
        ('Description', blocks.RichTextBlock(null = True))
    ])

    def child_pages(self):
        return Related_Projects.objects.live().child_of(self)

    search_fields = Page.search_fields + [
        index.SearchField('desc'),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('background'),
        StreamFieldPanel('desc'),
    ]

    # Specifies what content types can exist as children of BlogPage.
    # Empty list means that no child content types are allowed.
    subpage_types = ['related_projects.Related_Projects']

    class Meta:
        verbose_name = "General Projects Page"

    # Returns a queryset of Related_Projects objects that are live, that are direct
    # descendants of this index page with most recent first
    def get_projects(self):
        return Related_Projects.objects.live().descendant_of(
            self).order_by('-first_published_at')

    # Allows child objects (e.g. Related_Projects objects) to be accessible via the
    # template. We use this on the HomePage to display child items of featured
    # content
    def children(self):
        return self.get_children().specific().live()

    # Pagination for the index page. We use the `django.core.paginator` as any
    # standard Django app would, but the difference here being we have it as a
    # method on the model rather than within a view function
    def paginate(self, request, *args):
        page = request.GET.get('page')
        projects = args[0]
        search_query = args[1]
        if search_query:
            projects = projects.search(search_query)

            # Log the query so Wagtail can suggest promoted results
            Query.get(search_query).add_hit()

        paginator = Paginator(projects, 6)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        search_query = request.GET.get('query', None)

        context = super(General_Projects, self).get_context(request)
        context['projects'] = self.paginate(request, self.get_projects(), search_query)
        context['query'] = search_query

        return context

    #sets slug to op
    def full_clean(self, *args, **kwargs):
        super(General_Projects, self).full_clean(*args, **kwargs)

        if not self.slug.startswith('our-projects'):
            self.slug = 'our-projects'


class Related_Projects(Page):
    template = 'projects/project-page.html'
    desc = StreamField([
        ('Description', blocks.RichTextBlock(null = True)),
    ])

    background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    type = models.TextField()

    highlights = StreamField([
        ('Images', ImageChooserBlock(null=True)),
    ])

    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    date = models.DateField("Post date")

    search_fields = Page.search_fields + [
        index.SearchField('highlights'),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('background'),
        StreamFieldPanel('desc'),
        FieldPanel('type'),
        StreamFieldPanel('highlights'),
        FieldPanel('thumbnail'),
        FieldPanel('date'),
        InlinePanel('stories', heading='Related Stories')
    ]

    # Pagination for the index page. We use the `django.core.paginator` as any
    # standard Django app would, but the difference here being we have it as a
    # method on the model rather than within a view function
    def paginate(self, request, *args):
        page = request.GET.get('page')
        stories = args[0]
        paginator = Paginator(stories, 3)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        context = super(Related_Projects, self).get_context(request)
        stories = [
            n.story for n in self.stories.all()
        ]
        context['stories'] = self.paginate(request, stories)
        return context

    class Meta:
        verbose_name = "Related Projects Page"
        verbose_name_plural = "Related Projects Pages"

    #parent_page_types = ['related_projects.General_Projects']


class ProjectStories(Orderable):
    project = ParentalKey(
        'Related_Projects',
        related_name='stories',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    story = models.OneToOneField(OurStoriesSpecific, on_delete=models.CASCADE, null=True, blank=True)

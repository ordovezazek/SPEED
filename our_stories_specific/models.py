from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.core import blocks
from our_stories_specific.blocks import BaseStreamBlock
from wagtail.images.blocks import ImageChooserBlock
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search.models import Query
from django.shortcuts import render, redirect
# from related_projects.models import Related_Projects
from django import forms


class Comment(models.Model):
    post = models.ForeignKey('OurStoriesSpecific', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment By {}'.format(self.name)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs={
            'id' : 'fname',
            'placeholder' : 'John Smith'
        }
        self.fields['body'].widget.attrs={
            'id' : 'comment',
            'placeholder' : 'Write something...',
            'style': 'height: 200px'
        }


class General_Stories(Page):
    template = 'ourstoriesspecific/article_page.html'

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
        return OurStoriesSpecific.objects.live().child_of(self)

    search_fields = Page.search_fields + [
        index.SearchField('desc'),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('background'),
        StreamFieldPanel('desc'),
    ]

    # Specifies what content types can exist as children of BlogPage.
    # Empty list means that no child content types are allowed.
    subpage_types = ['our_stories_specific.OurStoriesSpecific']

    class Meta:
        verbose_name = "General Stories Page"

    # Returns a queryset of Related_Projects objects that are live, that are direct
    # descendants of this index page with most recent first
    def get_stories(self):
        return OurStoriesSpecific.objects.live().descendant_of(
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
        stories = args[0]
        search_query = args[1]
        if search_query:
            stories = stories.search(search_query)

            # Log the query so Wagtail can suggest promoted results
            Query.get(search_query).add_hit()

        paginator = Paginator(stories, 4)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        search_query = request.GET.get('search', None)

        context = super(General_Stories, self).get_context(request)
        context['stories'] = self.paginate(request, self.get_stories(), search_query)
        context['query'] = search_query

        return context

    #sets slug to oss
    def full_clean(self, *args, **kwargs):
        super(General_Stories, self).full_clean(*args, **kwargs)

        if not self.slug.startswith('our-stories'):
            self.slug = 'our-stories'



class OurStoriesSpecific(Page):

    template = 'ourstoriesspecific/our_stories_specific.html'

    # Database fields
    # project = models.ForeignKey(Related_Projects, null=True, blank=True, related_name='stories', on_delete=models.SET_NULL)
    background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    author = models.CharField(max_length=255, blank=True, null=True)
    introduction = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True,)
    date = models.DateField("Post date", blank=True, null=True)
    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )

    photos = StreamField([
        ('Images', ImageChooserBlock(null=True)),
    ], null=True, blank=True)

    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.FilterField('date'),
        index.SearchField('body'),

    ]

    def serve(self, request):
        comments = Comment.objects.filter(post=self).order_by('-created_on')
        if request.method == 'POST':
            form = CommentForm(request.POST)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = self
                comment.save()
                return redirect(self.url)
        else:
            form = CommentForm()

        return render(request, self.template, {
            'page': self,
            'comments': comments,
            'comment_form': form
        })

    # Editor panels configuration

    content_panels = Page.content_panels + [
        ImageChooserPanel('background'),

        MultiFieldPanel([
             FieldPanel('date'),
             FieldPanel('introduction'),
             ImageChooserPanel('thumbnail'),        
         ], heading="Post Details"),

        StreamFieldPanel('body', classname="full"),

        MultiFieldPanel([
            StreamFieldPanel('photos'),
        ], heading="Gallery"),

        # InlinePanel('related_links', label="Related links"),
    ]

    def __str__(self):
        return self.title

    @property
    def reading_length(self):
        count = 0
        if self.introduction:
            count = len(self.introduction.split())

        for block in self.body:
            if block.block_type != 'image_block':
                if block.value:
                    count += len(str(block.value).split())

        decimal = count / 200
        minutes = int(decimal)
        seconds = decimal % 1 * 0.60
        if seconds >= 0.30:
            minutes += 1

        return "{} minute".format(minutes) + ("s" if minutes > 1 else "") if minutes > 0 else "{} seconds".format(int(seconds * 100))



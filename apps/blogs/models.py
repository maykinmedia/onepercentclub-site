from django.conf import settings
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _


from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from djchoices import DjangoChoices, ChoiceItem
from fluent_contents.models import PlaceholderField
from fluent_contents.plugins.oembeditem.models import OEmbedItem
from fluent_contents.rendering import render_placeholder
from sorl.thumbnail import ImageField
from taggit_autocomplete_modified.managers import TaggableManagerAutocomplete as TaggableManager


from bluebottle.bluebottle_utils.serializers import MLStripper
from bluebottle.bluebottle_utils.utils import clean_for_hashtag
from bluebottle.geo.models import Country


from bluebottle.contentplugins.models import PictureItem


from .managers import BlogPostManager, BlogPostProxyManager


import re


class BlogCategory(models.Model):
    title = models.CharField(_("Title"), max_length=200)

    class Meta:
        verbose_name = _("Blog category")
        verbose_name_plural = _("Blog categories")

    def __unicode__(self):
        return self.title


# Based on https://github.com/edoburu/django-fluent-blogs/
# which doesn't offer custom base class models yet.
class BlogPost(models.Model):
    """
    Blog post / news item.
    """
    class PostStatus(DjangoChoices):
        published = ChoiceItem('published', label=_("Published"))
        draft = ChoiceItem('draft', label=_("Draft"))

    class PostType(DjangoChoices):
        blog = ChoiceItem('blog', label=_("Blog"))
        news = ChoiceItem('news', label=_("News"))

    post_type = models.CharField(_("Type"), max_length=20, choices=PostType.choices, db_index=True)
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"))

    # Contents
    main_image = ImageField(_("Main photo"), upload_to='blogs', blank=True)
    language = models.CharField(_("language"), max_length=5, choices=settings.LANGUAGES)
    contents = PlaceholderField("blog_contents")

    # Publication
    status = models.CharField(_('status'), max_length=20, choices=PostStatus.choices, default=PostStatus.draft, db_index=True)
    publication_date = models.DateTimeField(_('publication date'), null=True, db_index=True, help_text=_('''When the entry should go live, status must be "Published".'''))
    publication_end_date = models.DateTimeField(_('publication end date'), null=True, blank=True, db_index=True)
    allow_comments = models.BooleanField(_("Allow comments"), default=True)

    # Metadata
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('author'), editable=False)
    creation_date = CreationDateTimeField(_('creation date'))
    modification_date = ModificationDateTimeField(_('last modification'))

    # Taxonomy
    categories = models.ManyToManyField(BlogCategory, verbose_name=_("Categories"), blank=True)
    tags = TaggableManager(blank=True)
    countries = models.ManyToManyField(Country, verbose_name=_("Countries"), blank=True, null=True)

    objects = BlogPostManager()

    class Meta:
        verbose_name = _("Blog post")
        verbose_name_plural = _("Blog posts")
        unique_together = ('slug', 'language',)
        ordering = ('-publication_date', )

    def __unicode__(self):
        return self.title

    def get_meta_description(self, **kwargs):
        request = kwargs.get('request')
        s = MLStripper()
        s.feed(render_placeholder(request, self.contents))
        return truncatechars(s.get_data(), 250)

    def get_first_image(self, **kwargs):
        """
        For the facebook meta-data, the first image is required.

        Get all the content items and filter out those that are pictures.
        Return the url of the first picture.
        """
        relevant_items = [item for item in self.contents.get_content_items() \
                    if (isinstance(item, PictureItem) or isinstance(item, OEmbedItem))]
        
        item = relevant_items.pop(0)
        if isinstance(item, PictureItem):
            # we're sure we are dealing with a picture, so just return the image url
            request = kwargs.get('request')
            location = item.image.url
            absolute_uri = request.build_absolute_uri(location)
            return (absolute_uri, True)

        else:
            # it's an OEmbedItem. check if's an image suitable for facebook OG
            # https://developers.facebook.com/docs/web/tutorials/scrumptious/open-graph-object/
            # Only JPEG, PNG, GIF and BMP images are supported
            # TODO: a generic utils function for this kind of stuff would be nice ;)
            regex = re.compile(r'http(s?)://.*/.*\.(png|jpg|jpeg|jpe|jfif|jif|jfi|gif|bmp|dib)', re.IGNORECASE)
            match = re.match(regex, item.url)
            while relevant_items and not match:
                item = relevant_items.pop(0)
                match = re.match(regex, item.url)
            
            if match:
                # huray, we found a suitable image!
                return (item.url, True)
        return None

    def get_tweet(self, **kwargs):
        request = kwargs.get('request')
        lang_code = request.LANGUAGE_CODE
        twitter_handle = settings.TWITTER_HANDLES.get(lang_code, settings.DEFAULT_TWITTER_HANDLE)

        tweet = _(u"{title} {{URL}} via {twitter_handle}"
                    ).format(title=self.title, twitter_handle=twitter_handle)

        return tweet


# The proxy models are only here to have a separation in the Django admin interface.

class BlogPostProxy(BlogPost):
    """
    A subset of the ``BlogPost`` model that only displays real blog posts.
    """
    limit_to_post_type = BlogPost.PostType.blog
    objects = BlogPostProxyManager()

    class Meta:
        proxy = True
        verbose_name = _("Blog post")
        verbose_name_plural = _("Blog posts")

    def save(self, *args, **kwargs):
        self.post_type = self.limit_to_post_type
        super(BlogPostProxy, self).save(*args, **kwargs)


class NewsPostProxy(BlogPost):
    """
    A subset of the ``BlogPost`` model that only displays news items.
    """
    limit_to_post_type = BlogPost.PostType.news
    objects = BlogPostProxyManager()

    class Meta:
        proxy = True
        verbose_name = _("News")
        verbose_name_plural = _("News")

    def save(self, *args, **kwargs):
        self.post_type = self.limit_to_post_type
        super(NewsPostProxy, self).save(*args, **kwargs)

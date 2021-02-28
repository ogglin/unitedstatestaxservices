from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.fields import RichTextField

from wagtail.core.models import Page


class HomePage(Page):
    body = RichTextField(blank=True)
    html = StreamField([
        ('raw_html', blocks.RawHTMLBlock(blank=True, required=False)),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        StreamFieldPanel('html', classname="full"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request, *args, **kwargs)
        context['posts'] = self.path
        context['home_page'] = self

        context['menuitems'] = self.get_children().filter(
            live=True, show_in_menus=True)

        return context


class CategoryPage(Page):
    template = 'category/category_page.html'

    def get_context(self, request, *args, **kwargs):
        # context = super(CategoryPage, self).get_context(request, *args, **kwargs)
        context = super().get_context(request)
        context['posts'] = self.get_children().filter(live=True)
        context['page'] = self

        return context


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

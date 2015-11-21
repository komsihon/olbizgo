from amazon.models import AmazonConfig, Category
from cms.models import Config, FlatPage
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView


class BaseView(TemplateView):
    def get_context_data(self, **kwargs):
        configs = Config.objects.all()
        amazon_configs = AmazonConfig.objects.all()
        config = configs[0] if len(configs) > 0 else {}
        amazon_config = amazon_configs[0] if len(amazon_configs) > 0 else {'item_border': True}
        main_categories = Category.objects.filter(appear_in_main=True, visible=True)
        minor_categories = Category.objects.filter(appear_in_main=False, visible=True)
        categories = Category.objects.filter(home_previews_count__gt=0, visible=True)
        context = {
            'config': config,
            'amazon_config': amazon_config,
            'main_categories': main_categories,
            'minor_categories': minor_categories,
            'categories': categories
        }
        return context


class FlatPageView(BaseView):
    template_name = 'flat_page.html'

    def get_context_data(self, **kwargs):
        context = super(FlatPageView, self).get_context_data(**kwargs)
        slug = kwargs.get('slug')
        page = get_object_or_404(FlatPage, slug=slug)
        context['page'] = page
        return context
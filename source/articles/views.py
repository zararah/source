from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Article
from taggit.models import Tag

SECTION_MAP = {
    'articles': {
        'name': 'Articles', 
        'slug': 'articles',
        'article_types': ['project', 'tool', 'how-to',],
    },
    'community': {
        'name': 'Community', 
        'slug': 'community',
        'article_types': ['interview', 'roundtable', 'roundup', 'event', 'update'],
    },
}

CATEGORY_MAP = {
    'project': {
        'name': 'Project',
        'parent_name': 'Articles',
        'parent_slug': 'articles',
    },
    'tool': {
        'name': 'Tool',
        'parent_name': 'Articles',
        'parent_slug': 'articles',
    },
    'how-to': {
        'name': 'How-to',
        'parent_name': 'Articles',
        'parent_slug': 'articles',
    },
    'interview': {
        'name': 'Interview',
        'parent_name': 'Community',
        'parent_slug': 'community',
    },
    'roundtable': {
        'name': 'Roundtable',
        'parent_name': 'Community',
        'parent_slug': 'community',
    },
    'roundup': {
        'name': 'Roundup',
        'parent_name': 'Community',
        'parent_slug': 'community',
    },
    'event': {
        'name': 'Event',
        'parent_name': 'Community',
        'parent_slug': 'community',
    },
    'update': {
        'name': 'Update',
        'parent_name': 'Community',
        'parent_slug': 'community',
    },
}

class ArticleList(ListView):
    model = Article
    
    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        if self.section:
            context['section'] = SECTION_MAP[self.section]
            context['active_nav'] = SECTION_MAP[self.section]['slug']
        elif self.category:
            context['category'] = CATEGORY_MAP[self.category]['name']
            context['section'] = SECTION_MAP[CATEGORY_MAP[self.category]['parent_slug']]
            context['active_nav'] = CATEGORY_MAP[self.category]['parent_slug']
        elif self.tag:
            context['section'] = SECTION_MAP['articles']
            context['active_nav'] = SECTION_MAP['articles']['slug']
            context['tag'] = self.tag
        return context
    
    def get_queryset(self):
        # TODO add future date filters
        queryset = Article.objects.filter(is_live=True)
        self.section = self.kwargs.get('section', None)
        self.category = self.kwargs.get('category', None)
        self.tag_slug = self.kwargs.get('tag_slug', None)

        if self.section:
            queryset = queryset.filter(article_type__in=SECTION_MAP[self.section]['article_types'])
        elif self.category:
            queryset = queryset.filter(article_type=self.category)
        elif self.tag_slug:
            self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
            queryset = queryset.filter(tags__slug=self.kwargs['tag_slug'])
            
        return queryset


class ArticleDetail(DetailView):
    model = Article


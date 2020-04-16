from django.db.models import Count,Q
from .models import Category, Tag

def common(request):
    context = {
        'categories': Category.objects.annotate(
            num_post=Count('post', filter=Q(post__is_public=True))),

        'tags': Tag.objects.annotate(
            num_post=Count('post', filter=Q(post__is_public=True))),
    }

    return context

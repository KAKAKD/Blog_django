from django.urls import path
from .views import(
IndexView,
PostDetailView,
CategoryListView,
TagListView,
TagListView,
CategoryPostView,
TagPostView,
CommentFormView,
comment_approve,
comment_remove,
ReplyFormView,
reply_approve,
reply_remove,
SearchPostView,
)


app_name = 'blog_base'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('detail/<int:pk>', PostDetailView.as_view(), name='detail' ),
    path('category/', CategoryListView.as_view(), name='category' ),
    path('tag/', TagListView.as_view(), name='tag' ),
    path('category/<str:category_slug>', CategoryPostView.as_view(), name = 'category_post'),
    path('tag/<str:tag_slug>', TagPostView.as_view(), name = 'tag_post'),
    path('comment/<int:pk>',CommentFormView.as_view(),name='comment_form'),
    path('comment/<int:pk>/approve',comment_approve,name='comment_approve'),
    path('comment/<int:pk>/remove', comment_remove ,name='comment_remove'),
    path('reply/<int:pk>', ReplyFormView.as_view(),name='reply_form'),
    path('reply/<int:pk>/approve', reply_approve ,name='reply_approve'),
    path('reply/<int:pk>/remove', reply_remove ,name='reply_remove'),
    path('search/', SearchPostView.as_view(),name='search_post'),
]

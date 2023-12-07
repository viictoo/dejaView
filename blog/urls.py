from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='blog-home'), #function based view


    path('posts/', PostListView.as_view(), name='blog-home'), # class based view
    path('posts/user/<str:username>', UserPostListView.as_view(), name='user-posts'), # class based view
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), # class based viewX
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'), # class based viewX
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'), # class based viewX
    path('post/new/', PostCreateView.as_view(), name='post-create'), # class based view creae

    path('about/', views.about, name='blog-about')
]

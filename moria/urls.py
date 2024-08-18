from django.urls import path, include
from . views import *
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home, name='home'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('game/',game, name='game'),
    path('login/',ulogin, name='login'),
    path('signup/', signup, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('lessons/', lessons, name='lessons'),
    path('premium/', premium, name='premium'),
    path('notes/', notes, name='notes'),
    path('note1/', note1, name='note1'),
    path('profile/', profileview, name='profile'),
    path('kidsignup/', kidsignup, name='kidsignup'),
    path('medinator/', medinator, name='medinator'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
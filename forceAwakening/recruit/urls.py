from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', index),    
    path('questions/', questions),    
    path('welcome/', welcome),
    path('sith/', sith),
    path('sith/showRecruits/', showRecruits),
    path('sith/showAnswers/', showAnswers),
    path('sith/shadowHand/', shadowHand),
    # re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]
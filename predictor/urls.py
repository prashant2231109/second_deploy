from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('predict/', views.predict_view, name='predict_view'),
    
]
urlpatterns += staticfiles_urlpatterns()
from django.urls import path
from django.contrib import admin
from . import api
urlpatterns = [path('admin/',admin.site.urls)]
for route, view in [('auth/register',api.register),('auth/login',api.login),('auth/logout',api.logout),('farmers/me',api.me),('farms',api.farms),('advisory/ask',api.ask),('crop-diagnosis',api.diagnosis),('weather',api.weather),('market-prices',api.market),('feedback',api.feedback),('expert-cases',api.cases),('admin/analytics',api.analytics),('whatsapp/webhook',api.whatsapp)]:
    urlpatterns.append(path('api/'+route,view))
urlpatterns += [path('api/expert-cases/<int:pk>/respond',api.respond),path('api/crop-diagnosis/<int:pk>/image',api.diagnosis_image)]

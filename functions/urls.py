from django.urls import path
from .Actions import root
from .Actions import uploads
from .Actions import fileActions

urlpatterns = [
    path('', root.root),
    path('uploads', uploads.upload),
    path('actions', fileActions.fileAction)
]

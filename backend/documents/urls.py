from django.urls import path
from .views import (
    document_list, document_detail, share_document,
    import_document, recent_activity,
    document_attachments, attachment_detail,
    import_into_document,
)

urlpatterns = [
    path('', document_list, name='document-list'),
    path('<int:doc_id>/', document_detail, name='document-detail'),
    path('<int:doc_id>/share/', share_document, name='document-share'),
    path('import/', import_document, name='document-import'),
    path('activity/', recent_activity, name='document-activity'),
    # Feature 2 — Attachments
    path('<int:doc_id>/attachments/', document_attachments, name='document-attachments'),
    path('<int:doc_id>/attachments/<int:att_id>/', attachment_detail, name='attachment-detail'),
    # Feature 3 — Import into existing draft
    path('<int:doc_id>/import/', import_into_document, name='import-into-document'),
]

from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Document, DocumentShare, DocumentAttachment
from .serializers import DocumentSerializer, DocumentShareSerializer, DocumentAttachmentSerializer
from .services import FileImportService, DocumentService
import json
from itertools import chain
from operator import attrgetter


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def document_list(request):
    """Get all documents (owned and shared) or create a new document"""
    if request.method == 'GET':
        owned_documents = Document.objects.filter(owner=request.user)
        shared_documents = Document.objects.filter(shares__shared_with=request.user)
        
        owned_serializer = DocumentSerializer(owned_documents, many=True)
        shared_serializer = DocumentSerializer(shared_documents, many=True)
        
        return Response({
            'owned': owned_serializer.data,
            'shared': shared_serializer.data,
        })
    
    elif request.method == 'POST':
        data = request.data
        if not data.get('title'):
            return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        document = Document.objects.create(
            title=data['title'],
            content={},
            owner=request.user
        )
        serializer = DocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def document_detail(request, doc_id):
    """Get, update, or delete a specific document"""
    try:
        document = Document.objects.get(id=doc_id)
    except Document.DoesNotExist:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check authorization: owner or shared with
    is_owner = document.owner == request.user
    is_shared = DocumentShare.objects.filter(document=document, shared_with=request.user).exists()
    
    if request.method == 'GET':
        if not (is_owner or is_shared):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        serializer = DocumentSerializer(document)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # if not is_owner:
        #     return Response({'error': 'Only owner can edit'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        if 'title' in data:
            document.title = data['title']
        if 'content' in data:
            document.content = data['content']
        
        document.save()
        serializer = DocumentSerializer(document)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if not is_owner:
            return Response({'error': 'Only owner can delete'}, status=status.HTTP_403_FORBIDDEN)
        
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_document(request, doc_id):
    """Share document with another user"""
    try:
        document = Document.objects.get(id=doc_id)
    except Document.DoesNotExist:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # if document.owner != request.user:
    #     return Response({'error': 'Only owner can share'}, status=status.HTTP_403_FORBIDDEN)
    
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if email == request.user.email:
        return Response({'error': 'Cannot share with yourself'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if already shared
    if DocumentShare.objects.filter(document=document, shared_with=user).exists():
        return Response({'error': 'Already shared with this user'}, status=status.HTTP_400_BAD_REQUEST)
    
    share = DocumentShare.objects.create(document=document, shared_with=user)
    serializer = DocumentShareSerializer(share)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_document(request):
    """Import a document from .txt or .md file — creates a new document"""
    if 'file' not in request.FILES:
        return Response({'error': 'File is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    title = request.data.get('title', file.name.split('.')[0])
    
    # Validate file type
    if not (file.name.endswith('.txt') or file.name.endswith('.md') or file.name.endswith('.docx')):
        return Response({'error': 'Only .txt, .md, and .docx files are supported'}, status=status.HTTP_400_BAD_REQUEST)
    
    if file.name.endswith('.docx'):
        try:
            tiptap_content = FileImportService.convert_docx_to_tiptap(file)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Read file content for plain text
        try:
            content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            return Response({'error': 'File encoding error'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not content.strip():
            return Response({'error': 'File is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Convert to Tiptap JSON format
        try:
            tiptap_content = FileImportService.convert_to_tiptap(content)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create document
    document = Document.objects.create(
        title=title,
        content=tiptap_content,
        owner=request.user
    )
    
    serializer = DocumentSerializer(document)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# ─────────────────────────────────────────────
#  Feature 2: Attachments for an existing document
# ─────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def document_attachments(request, doc_id):
    """List or upload attachments for a specific document"""
    try:
        document = Document.objects.get(id=doc_id)
    except Document.DoesNotExist:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

    is_owner = document.owner == request.user
    is_shared = DocumentShare.objects.filter(document=document, shared_with=request.user).exists()

    if not (is_owner or is_shared):
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        attachments = DocumentAttachment.objects.filter(document=document)
        serializer = DocumentAttachmentSerializer(attachments, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        if 'file' not in request.FILES:
            return Response({'error': 'File is required'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']

        # 20 MB size limit
        if file.size > 20 * 1024 * 1024:
            return Response({'error': 'File must be smaller than 20 MB'}, status=status.HTTP_400_BAD_REQUEST)

        mime_type = file.content_type or ''

        attachment = DocumentAttachment.objects.create(
            document=document,
            uploaded_by=request.user,
            file=file,
            filename=file.name,
            file_size=file.size,
            mime_type=mime_type,
        )
        serializer = DocumentAttachmentSerializer(attachment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def attachment_detail(request, doc_id, att_id):
    """Delete a specific attachment"""
    try:
        document = Document.objects.get(id=doc_id)
    except Document.DoesNotExist:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        attachment = DocumentAttachment.objects.get(id=att_id, document=document)
    except DocumentAttachment.DoesNotExist:
        return Response({'error': 'Attachment not found'}, status=status.HTTP_404_NOT_FOUND)

    # Only the uploader or document owner can delete
    if attachment.uploaded_by != request.user and document.owner != request.user:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

    # Remove physical file from storage
    attachment.file.delete(save=False)
    attachment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ─────────────────────────────────────────────
#  Feature 3: Import file content into an existing draft
# ─────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_into_document(request, doc_id):
    """
    Import content from a .txt / .md / .docx file into an existing document.
    mode=append  -> append imported paragraphs after existing content  (default)
    mode=replace -> replace existing content entirely
    """
    try:
        document = Document.objects.get(id=doc_id)
    except Document.DoesNotExist:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

    if document.owner != request.user:
        return Response({'error': 'Only the owner can import content'}, status=status.HTTP_403_FORBIDDEN)

    if 'file' not in request.FILES:
        return Response({'error': 'File is required'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']
    mode = request.data.get('mode', 'append')  # 'append' or 'replace'

    if not (file.name.endswith('.txt') or file.name.endswith('.md') or file.name.endswith('.docx')):
        return Response({'error': 'Only .txt, .md, and .docx files are supported'}, status=status.HTTP_400_BAD_REQUEST)

    # Convert uploaded file to Tiptap JSON
    if file.name.endswith('.docx'):
        try:
            imported_tiptap = FileImportService.convert_docx_to_tiptap(file)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            text_content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            return Response({'error': 'File encoding error'}, status=status.HTTP_400_BAD_REQUEST)

        if not text_content.strip():
            return Response({'error': 'File is empty'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            imported_tiptap = FileImportService.convert_to_tiptap(text_content)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    imported_nodes = imported_tiptap.get('content', [])

    if mode == 'replace':
        document.content = imported_tiptap
    else:
        # Append mode: merge imported nodes after existing ones
        existing_content = document.content or {}
        existing_nodes = existing_content.get('content', [])
        document.content = {
            'type': 'doc',
            'content': existing_nodes + imported_nodes,
        }

    document.save()
    serializer = DocumentSerializer(document)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent_activity(request):
    """Return recent activity events for the current user"""
    events = []

    # --- Owned documents: created & edited ---
    owned_docs = Document.objects.filter(owner=request.user).order_by('-updated_at')[:20]
    for doc in owned_docs:
        # If created_at == updated_at (within 1 second), treat as 'created'
        delta = abs((doc.updated_at - doc.created_at).total_seconds())
        if delta < 2:
            events.append({
                'type': 'created',
                'timestamp': doc.created_at.isoformat(),
                'document_id': doc.id,
                'document_title': doc.title,
                'actor': 'You',
                'actor_email': request.user.email,
            })
        else:
            events.append({
                'type': 'edited',
                'timestamp': doc.updated_at.isoformat(),
                'document_id': doc.id,
                'document_title': doc.title,
                'actor': 'You',
                'actor_email': request.user.email,
            })

    # --- Shares made by the user (you shared a doc with someone) ---
    outgoing_shares = DocumentShare.objects.filter(
        document__owner=request.user
    ).select_related('document', 'shared_with').order_by('-created_at')[:20]
    for share in outgoing_shares:
        events.append({
            'type': 'shared_out',
            'timestamp': share.created_at.isoformat(),
            'document_id': share.document.id,
            'document_title': share.document.title,
            'actor': 'You',
            'actor_email': request.user.email,
            'target_email': share.shared_with.email,
        })

    # --- Shares received (someone shared a doc with you) ---
    incoming_shares = DocumentShare.objects.filter(
        shared_with=request.user
    ).select_related('document', 'document__owner').order_by('-created_at')[:20]
    for share in incoming_shares:
        events.append({
            'type': 'shared_in',
            'timestamp': share.created_at.isoformat(),
            'document_id': share.document.id,
            'document_title': share.document.title,
            'actor': share.document.owner.username,
            'actor_email': share.document.owner.email,
        })

    # Sort all events by timestamp descending, return top 10
    events.sort(key=lambda x: x['timestamp'], reverse=True)
    return Response(events[:10], status=status.HTTP_200_OK)

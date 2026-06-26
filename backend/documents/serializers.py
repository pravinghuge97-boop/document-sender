from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
from .models import Document, DocumentShare, DocumentAttachment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class DocumentAttachmentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    uploaded_by_email = serializers.CharField(source='uploaded_by.email', read_only=True)

    class Meta:
        model = DocumentAttachment
        fields = ('id', 'filename', 'file_size', 'mime_type', 'url', 'uploaded_by_email', 'uploaded_at')
        read_only_fields = ('id', 'uploaded_at', 'uploaded_by_email')

    def get_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class DocumentSerializer(serializers.ModelSerializer):
    owner_email = serializers.CharField(source='owner.email', read_only=True)
    shared_with = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ('id', 'title', 'content', 'owner', 'owner_email', 'created_at', 'updated_at', 'shared_with')
        read_only_fields = ('owner', 'created_at', 'updated_at', 'shared_with')

    def get_shared_with(self, obj):
        shares = obj.shares.all()
        return [
            {
                'id': share.shared_with.id,
                'email': share.shared_with.email,
                'username': share.shared_with.username,
            }
            for share in shares
        ]


class DocumentShareSerializer(serializers.ModelSerializer):
    shared_with = UserSerializer(read_only=True)

    class Meta:
        model = DocumentShare
        fields = ('id', 'document', 'shared_with', 'created_at')
        read_only_fields = ('created_at',)

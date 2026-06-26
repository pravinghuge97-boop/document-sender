from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework import status
from .models import Document
import json


class DocumentCreationTest(TestCase):
    """Test document creation flow"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_document_creation_flow(self):
        """Test creating, retrieving, updating, and deleting a document"""
        
        # Step 1: Login
        login_response = self.client.post(
            '/api/auth/login/',
            {'email': 'test@example.com', 'password': 'testpass123'},
            content_type='application/json'
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.json()['access']

        # Step 2: Create document
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        create_response = self.client.post(
            '/api/documents/',
            {'title': 'Test Document'},
            content_type='application/json',
            **headers
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        doc_id = create_response.json()['id']

        # Step 3: Retrieve document
        get_response = self.client.get(
            f'/api/documents/{doc_id}/',
            **headers
        )
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.json()['title'], 'Test Document')

        # Step 4: Update document
        update_data = {
            'title': 'Updated Document',
            'content': {
                'type': 'doc',
                'content': [
                    {
                        'type': 'paragraph',
                        'content': [{'type': 'text', 'text': 'Hello World'}]
                    }
                ]
            }
        }
        update_response = self.client.put(
            f'/api/documents/{doc_id}/',
            json.dumps(update_data),
            content_type='application/json',
            **headers
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.json()['title'], 'Updated Document')

        # Step 5: List documents
        list_response = self.client.get(
            '/api/documents/',
            **headers
        )
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.json()['owned']), 1)

        # Step 6: Delete document
        delete_response = self.client.delete(
            f'/api/documents/{doc_id}/',
            **headers
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify deletion
        final_list = self.client.get(
            '/api/documents/',
            **headers
        )
        self.assertEqual(len(final_list.json()['owned']), 0)

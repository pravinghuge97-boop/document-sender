class FileImportService:
    """Service for converting files to Tiptap JSON format"""
    
    @staticmethod
    def convert_to_tiptap(text_content):
        """Convert plain text to Tiptap JSON format"""
        lines = text_content.strip().split('\n')
        content = []
        
        for line in lines:
            if not line.strip():
                # Empty line
                content.append({
                    "type": "paragraph",
                    "content": []
                })
            else:
                # Regular paragraph
                content.append({
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": line.strip()
                        }
                    ]
                })
        
        return {
            "type": "doc",
            "content": content
        }

    @staticmethod
    def convert_docx_to_tiptap(file_obj):
        """Convert DOCX file to Tiptap JSON format"""
        try:
            import docx
            import io
            file_obj.seek(0)
            file_buffer = io.BytesIO(file_obj.read())
            doc = docx.Document(file_buffer)
            content = []
            
            for paragraph in doc.paragraphs:
                if not paragraph.text.strip():
                    # Empty line
                    content.append({
                        "type": "paragraph",
                        "content": []
                    })
                else:
                    # Regular paragraph
                    content.append({
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": paragraph.text.strip()
                            }
                        ]
                    })

            
            # If document was entirely empty, provide at least one paragraph
            if not content:
                content.append({"type": "paragraph", "content": []})
                
            return {
                "type": "doc",
                "content": content
            }
        except Exception as e:
            raise Exception(f"Invalid or corrupted DOCX file: {str(e)}")

class DocumentService:
    """Service for document operations"""
    
    @staticmethod
    def create_empty_document():
        """Return empty Tiptap document"""
        return {
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": []
                }
            ]
        }

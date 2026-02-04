import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class LinkedInPublisher:
    def __init__(self, access_token=None):
        self.access_token = access_token or os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.base_url = "https://api.linkedin.com"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
            "Linkedin-Version": "202510"
        }

    def get_user_id(self):
        """
        Fetches the LinkedIn member ID (URN).
        """
        # Note: /v2/userinfo is still valid for sub (ID)
        response = requests.get(f"{self.base_url}/v2/userinfo", headers=self.headers)
        if response.status_code == 200:
            user_id = response.json().get('sub')
            return f"urn:li:person:{user_id}"
        else:
            return f"Error obteniendo ID: {response.text}"

    def initialize_image_upload(self, user_urn):
        """
        Step 1: Initialize image upload (Modern REST API).
        """
        url = f"{self.base_url}/rest/images?action=initializeUpload"
        payload = {
            "initializeUploadRequest": {
                "owner": user_urn
            }
        }
        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            image_urn = data["value"]["image"]
            upload_url = data["value"]["uploadUrl"]
            return image_urn, upload_url
        else:
            print(f"DEBUG: initialize_image_upload failed: {response.status_code} - {response.text}")
            return None, None

    def upload_image_binary(self, upload_url, image_path):
        """
        Step 2: Upload the binary image data.
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/octet-stream"
        }
        with open(image_path, "rb") as f:
            binary_data = f.read()
            response = requests.put(upload_url, headers=headers, data=binary_data)
            print(f"DEBUG: Image upload status: {response.status_code}")
            return response.status_code == 201 or response.status_code == 200

    def initialize_document_upload(self, user_urn, file_path):
        """
        Step 1: Initialize document upload.
        """
        url = f"{self.base_url}/rest/documents?action=initializeUpload"
        # The owner is the only strictly required field in the request body for this version.
        payload = {
            "initializeUploadRequest": {
                "owner": user_urn
            }
        }
        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            document_urn = data["value"]["document"]
            upload_url = data["value"]["uploadUrl"]
            return document_urn, upload_url
        else:
            print(f"DEBUG: initialize_document_upload failed: {response.status_code} - {response.text}")
            return None, None

    def upload_document_binary(self, upload_url, file_path):
        """
        Step 2: Upload the binary PDF data.
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/pdf"
        }
        with open(file_path, "rb") as f:
            binary_data = f.read()
            response = requests.put(upload_url, headers=headers, data=binary_data)
            return response.status_code == 200 or response.status_code == 201

    def post_content(self, text, image_path=None, pdf_path=None, title="Authority Content"):
        """
        Publishes a post (image, carousel/pdf, or text) to LinkedIn.
        """
        user_urn = self.get_user_id()
        if "Error" in user_urn:
            return user_urn

        asset_urn = None
        media_type = None

        # Opción 1: Carrusel (PDF/Documento) - PRIORIDAD
        if pdf_path and os.path.exists(pdf_path):
            asset_urn, upload_url = self.initialize_document_upload(user_urn, pdf_path)
            if asset_urn and upload_url:
                success = self.upload_document_binary(upload_url, pdf_path)
                if success:
                    media_type = "DOCUMENT"
                    import time
                    time.sleep(5) 
        
        # Opción 2: Imagen única (si no hay PDF)
        if not asset_urn and image_path and os.path.exists(image_path):
            asset_urn, upload_url = self.initialize_image_upload(user_urn)
            if asset_urn and upload_url:
                success = self.upload_image_binary(upload_url, image_path)
                if success:
                    media_type = "IMAGE"
                    import time
                    time.sleep(5)

        url = f"{self.base_url}/rest/posts"
        payload = {
            "author": user_urn,
            "commentary": text,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "lifecycleState": "PUBLISHED"
        }

        if media_type == "DOCUMENT":
            payload["content"] = {
                "media": {
                    "title": title,
                    "id": asset_urn
                }
            }
        elif media_type == "IMAGE":
            payload["content"] = {
                "media": {
                    "title": title,
                    "id": asset_urn
                }
            }

        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code == 201:
            try:
                import urllib.parse
                post_urn = urllib.parse.unquote(response.headers.get("x-restli-id"))
                return f"SUCCESS:{post_urn}"
            except:
                return "SUCCESS:Post published (ID not captured)"
        else:
            return f"Error al publicar: {response.text}"

    def post_comment(self, post_urn, comment_text, author_name=None):
        """
        Publishes a comment. If author_name is provided, it attempts to format a mention.
        Note: Real LinkedIn mentions require a specific URN format (urn:li:person:ID).
        For now, we use a clean text tag.
        """
        url = f"{self.base_url}/rest/comments"
        
        # Si tenemos un nombre, nos aseguramos de que el texto no tenga espacios raros tras el @
        if author_name and f"@{author_name}" in comment_text:
            clean_tag = f"@{author_name.replace(' ', '')}"
            comment_text = comment_text.replace(f"@{author_name}", clean_tag)

        payload = {
            "actor": self.get_user_id(),
            "object": post_urn,
            "message": {
                "text": comment_text
            }
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return response.status_code == 201

if __name__ == "__main__":
    # Test (needs token)
    publisher = LinkedInPublisher()
    # print(publisher.post_content("¡Hola! Este es un post automático de prueba desde mi bot de IA."))

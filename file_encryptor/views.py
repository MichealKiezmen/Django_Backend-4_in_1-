import os
from django.shortcuts import render
from rest_framework.views import APIView
from cryptography.fernet import Fernet
import pymupdf
from django.conf import settings


class Encryptor(APIView):
    
    def get(self, request):
        pass
    
    def post(self, request):
        
        key = Fernet.generate_key()
        f = Fernet(key)
        
        uploaded_file = request.FILES["document"]
        save_path = os.path.join(settings.MEDIA_ROOT, "uploads", uploaded_file.name)
                
        # CREATE THE PDF FILE
        with open(save_path, "wb+") as file:
            for chunk in uploaded_file.chunks():
                file.write(chunk)
                
        # READ THE PDF FILE AS BINARY
        with open(save_path, "rb") as file:
            data = file.read()

        #ENCRYPT THE BINARY DATA
        encrypted_data = f.encrypt(data)

        filename = uploaded_file.name.split(".")
        encrypted_save_path = os.path.join(settings.MEDIA_ROOT, "uploads", filename[0])
        with open(f"{encrypted_save_path}_22.txt", "wb+") as file2:
            file2.write(encrypted_data)
            
        #Upload file to CLoudinary
        #Delete files
        #Save file urls alongside the key

class Decryptor(APIView):
    
    def get(self, request):
        pass
    
    def post(self, request):
        key = request.data["key"]
        document = request.FILES["document"]
        f = Fernet(key)
        # with open(f"{encrypted_save_path}_22.txt", "rb") as file:
        #     tree_data = file.read()
        # cds = f.decrypt(tree_data)
        # with open(f"{encrypted_save_path}_22.pdf", "wb+") as file:
        #         file.write(cds)key

        
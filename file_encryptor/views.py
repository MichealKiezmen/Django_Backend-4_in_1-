import os
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from cryptography.fernet import Fernet
from user.models import User
from django.shortcuts import get_object_or_404
from django.conf import settings
from backend_django.reusable_classes import DriveClass
from .serializers import FileEncryptModelSerializer
from .models import FileEncryptModel
from user.services import token_required


drive_upload = DriveClass()

class Encryptor(APIView):

    @token_required
    def get(self, request, user_id):
        found_data = FileEncryptModel.objects.filter(user=user_id)
        serializer = FileEncryptModelSerializer(found_data, many=True).data
        return Response({"data" : serializer }, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        try:
            key = Fernet.generate_key()
            f = Fernet(key)
            user_found = User.objects.filter(id=user_id).first()
            uploaded_file = request.FILES["document"]
            returned_file_type = request.data.get("file_extension")
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
            with open(f"{encrypted_save_path}.{returned_file_type}", "wb+") as file2:
                file2.write(encrypted_data)

            file_id = drive_upload.upload_file(f"{encrypted_save_path}.{returned_file_type}", f"{filename[0]}.{returned_file_type}")
            file_url = drive_upload.get_file_url(file_id)

            if file_url is not None:
                res = drive_upload.delete_file_after_upload(f"{encrypted_save_path}.{returned_file_type}")
                res2 = drive_upload.delete_file_after_upload(save_path)

            result = {
                "encryption_key": str(key),
                "file_url": file_url,
                "google_drive_file_id": file_id,
                "user": user_id,
                "file_extension": filename[1],
                "file_name": uploaded_file.name
            }
            if user_found:
                serialized_data = FileEncryptModelSerializer(data=result)
                if serialized_data.is_valid():
                    serialized_data.save()
                    return Response(serialized_data.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error encrypting:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class EncryptionActionsView(APIView):

    @token_required
    def delete(self, request, data_id):
        found = get_object_or_404(FileEncryptModel, file_id=data_id)
        error_msg = True

        if found:
            result = drive_upload.delete_file_from_google_drive(found.google_drive_file_id)
            if result:
                error_msg = False
                found.delete()

        if error_msg:
            return Response({"error" : "File deletion unsuccessful" }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message" : "File deleted successfully" }, status=status.HTTP_200_OK)


class Decryptor(APIView):

    def get(self, request):
        pass

    def post(self, request):
        try:
            key = request.data["key"]
            cleaned_key = key.strip("b'").strip("'").encode()
            document = request.FILES["document"]
            f = Fernet(cleaned_key)

            key_found = FileEncryptModel.objects.filter(encryption_key=key).first()
            if not key_found:
                return Response({"error": "Wrong Decryption key."}, status=status.HTTP_404_NOT_FOUND)

            save_path = os.path.join(settings.MEDIA_ROOT, "uploads", document.name)

            # CREATE THE  FILE
            with open(save_path, "wb+") as file:
                for chunk in document.chunks():
                    file.write(chunk)

            # READ THE FILE AS BINARY
            with open(save_path, "rb") as file:
                data = file.read()

            decrypted = f.decrypt(data)
            new_filename = save_path.rsplit(".", 1)[0]

            with open(f"{new_filename}_decrypted.{key_found.file_extension}", "wb+") as file:
                    file.write(decrypted)

            filename = document.name.split(".")
            file_id = drive_upload.upload_file(
                f"{new_filename}_decrypted.{key_found.file_extension}",
                f"{filename[0]}.{key_found.file_extension}"
                )
            file_url = drive_upload.get_file_url(file_id)

            if file_url is not None:
                res = drive_upload.delete_file_after_upload(f"{new_filename}_decrypted.{key_found.file_extension}")
                res2 = drive_upload.delete_file_after_upload(save_path)

            result = {
                "file_url": file_url,
            }
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error encrypting:", str(e))
            return Response({"error": str(e) or f"The decryption key provided has no relation to the file: {document.name}."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

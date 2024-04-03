import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AudioModel
from .serializers import AudioDataSerializers
from .save_audio import AudioToURL
from .get_audio import string_to_convert, speech, delete_file_after_upload
from django.views.decorators.csrf import csrf_exempt


audio_instance = AudioToURL()



# Create your views here.
class PDF_To_TextAPI(APIView):
    def get(self, request):
        user_links = AudioModel.objects.all()
        serializer_user_links = AudioDataSerializers(user_links, many=True)
        data = {
            "data":serializer_user_links.data,
            "message":"Fetched Successfully."

        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        uploaded_file = request.FILES['pdf']  # 'pdf' is the name attribute of your file input
        #Create a path to save the file
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', uploaded_file.name)
        with open(save_path, 'wb+') as destination:
            #loop through the chunks property of data in the  client file upload
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        text = string_to_convert(save_path)  #All texts contained in the PDF
        if text:
            file_name = uploaded_file.name.split(".")
            audio_file_path = speech(text,file_name[0])
            print(type(audio_file_path))

            if audio_file_path:
                data = audio_instance.upload_audio(audio_file_path, f"{file_name[0]}.mp3")
                print(type(data))
                link = audio_instance.get_audio_url(data)
            else:
                return Response({
                    "message": "Ooops, Something went wrong with the server!"
                }, status=status.HTTP_400_BAD_REQUEST)

            #  # Check if the file exists before trying to delete it
            is_audio_deleted = delete_file_after_upload(audio_file_path)
            is_pdf_deleted = delete_file_after_upload(save_path)

            new_data = AudioModel(
                url=link
            )

            new_data.save()
            response = {
                "link": link,
                "message":"PDF Successfully converted"
            }
            return Response(response, status=status.HTTP_200_OK)


# @csrf_exempt

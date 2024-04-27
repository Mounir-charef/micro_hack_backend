from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from summary.models import Summarizer
from summary.serializers import SummarizerSerializer
from summary.summarize import summarize_text, calculate_scores
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import status


class SummarizerView(ReadOnlyModelViewSet):
    queryset = Summarizer.objects.all()
    serializer_class = SummarizerSerializer

    def create(self, request, *args, **kwargs):
        uploaded_file = request.data.get("text")

        if not uploaded_file:
            return Response(
                {"error": "No text file provided."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check if uploaded_file is a file
        if not isinstance(uploaded_file, InMemoryUploadedFile):
            return Response(
                {"error": "Invalid file type. Only .txt files are allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the file is a text file
        if not uploaded_file.name.endswith(".txt"):
            return Response(
                {"error": "Invalid file type. Only .txt files are allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            text = uploaded_file.read().decode("utf-8")
        except UnicodeDecodeError:
            return Response(
                {"error": "Unable to decode the file."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        summary = summarize_text(text)

        scores = calculate_scores(text, summary)
        try:
            serializer = self.get_serializer(
                data={
                    "text": uploaded_file,
                    "summary": summary,
                    "scores": scores,
                }
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

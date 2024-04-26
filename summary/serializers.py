from rest_framework import serializers

from summary.models import Summarizer


class SummarizerSerializer(serializers.ModelSerializer):
    text = serializers.FileField(
        required=True,
        allow_empty_file=False,
        use_url=False,
    )

    class Meta:
        model = Summarizer
        fields = "__all__"

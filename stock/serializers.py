from rest_framework import serializers

from stock.models import Snippet


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = [ 'title', 'code', 'linenos']
from rest_framework import serializers

from . import validators
from .models import Document
from .models import Paragraph


class ParagraphSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=Paragraph._meta.get_field('name').max_length
    )
    weight = serializers.IntegerField()
    text = serializers.CharField()


class DocumentSerializer(serializers.ModelSerializer):
    paragraphs = ParagraphSerializer(many=True, partial=True)

    class Meta:
        model = Document
        exclude = ('creator',)

    def validate(self, data):
        if self.instance:
            document_pk = self.instance.pk
        else:
            document_pk = None
        validators.single_document_per_module(data['module'], document_pk)
        return data

    def create(self, validated_data):
        paragraphs = validated_data.pop('paragraphs')
        user = self.context['request'].user
        document = Document.objects.create(creator=user, **validated_data)

        for paragraph in paragraphs:
            Paragraph.objects.create(document=document, **paragraph)

        return document

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.save()
        paragraphs = validated_data.pop('paragraphs')

        paragraph_ids = [item['id'] for item in paragraphs if 'id' in item]
        instance.paragraphs.exclude(id__in=paragraph_ids).delete()

        for paragraph in paragraphs:
            paragraph['document'] = instance
            if 'id' in paragraph:
                instance.paragraphs.filter(id=paragraph['id'])\
                                   .update(**paragraph)
            else:
                instance.paragraphs.create(**paragraph)

        return instance

from rest_framework import serializers

from adhocracy4.modules.models import Module

from .models import Chapter
from .models import Paragraph


class ParagraphSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    name = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=Paragraph._meta.get_field('name').max_length
    )

    class Meta:
        model = Paragraph
        fields = ('id', 'weight', 'name', 'text')


class ChapterListSerializer(serializers.ListSerializer):
    def create_or_update(self, validated_data):
        chapter_ids = [chapter['id']
                       for chapter in validated_data
                       if 'id' in chapter]
        Chapter.objects\
            .filter(module_id=self.context['module_pk'])\
            .exclude(id__in=chapter_ids)\
            .delete()

        for weight, chapter in enumerate(validated_data):
            chapter['weight'] = weight
            if 'id' in chapter:
                instance = Chapter.objects.get(id=chapter['id'])
                yield self.child.update(instance, chapter)
            else:
                yield self.child.create(chapter)

    def create(self, validated_data):
        return list(self.create_or_update(validated_data))


class ChapterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    paragraphs = ParagraphSerializer(many=True)

    class Meta:
        model = Chapter
        fields = ('id', 'name', 'weight', 'paragraphs')
        list_serializer_class = ChapterListSerializer

    def validate(self, data):
        module_pk = self.context['module_pk']
        module = Module.objects.get(pk=module_pk)
        data['module'] = module
        return data

    def create(self, validated_data):
        paragraphs = validated_data.pop('paragraphs')
        user = self.context['request'].user
        chapter = Chapter.objects.create(creator=user, **validated_data)

        for paragraph in paragraphs:
            Paragraph.objects.create(chapter=chapter, **paragraph)

        return chapter

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.weight = validated_data['weight']
        instance.save()
        paragraphs = validated_data.pop('paragraphs')

        paragraph_ids = [item['id'] for item in paragraphs if 'id' in item]
        instance.paragraphs.exclude(id__in=paragraph_ids).delete()

        for paragraph in paragraphs:
            paragraph['chapter'] = instance
            if 'id' in paragraph:
                instance.paragraphs.filter(id=paragraph['id'])\
                                   .update(**paragraph)
            else:
                instance.paragraphs.create(**paragraph)

        return instance


class DocumentSerializer(serializers.Serializer):
    chapters = ChapterSerializer(many=True)

    def create(self, validated_data):
        chapters = self.fields['chapters'].create(validated_data['chapters'])
        return {
            'chapters': sorted(chapters, key=lambda chapter: chapter.weight)
        }

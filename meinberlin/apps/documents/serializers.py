from rest_framework import serializers

from adhocracy4.dashboard import components
from adhocracy4.dashboard import signals as a4dashboard_signals
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
        extra_kwargs = {
            'weight': {'required': False, 'default': 0, 'write_only': True}
        }


class ChapterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    paragraphs = ParagraphSerializer(many=True)

    class Meta:
        model = Chapter
        fields = ('id', 'name', 'weight', 'paragraphs')
        extra_kwargs = {
            'weight': {'required': False, 'default': 0, 'write_only': True}
        }

    def create(self, validated_data):
        paragraphs = validated_data.pop('paragraphs')
        user = self.context['request'].user
        module = Module.objects.get(pk=self.context['module_pk'])
        chapter = Chapter.objects.create(creator=user,
                                         module=module,
                                         **validated_data)

        for weight, paragraph_data in enumerate(paragraphs):
            paragraph_data['weight'] = weight
            Paragraph.objects.create(chapter=chapter,
                                     **paragraph_data)

        return chapter

    def update(self, instance, validated_data):
        # Update the chapter
        paragraphs_data = validated_data.pop('paragraphs')
        chapter = super(ChapterSerializer, self)\
            .update(instance, validated_data)

        # Delete removed paragraphs from the database
        paragraph_ids = [item['id']
                         for item in paragraphs_data
                         if 'id' in item]
        chapter.paragraphs.exclude(id__in=paragraph_ids).delete()

        # Update or create the chapters
        for weight, paragraph_data in enumerate(paragraphs_data):
            paragraph_data['weight'] = weight
            if 'id' in paragraph_data:
                paragraph = Paragraph.objects.get(id=paragraph_data['id'])
                assert paragraph.chapter == chapter
                Paragraph.objects\
                    .filter(id=paragraph.id)\
                    .update(**paragraph_data)

            else:
                Paragraph.objects.create(chapter=chapter,
                                         **paragraph_data)

        return chapter


class DocumentSerializer(serializers.Serializer):
    chapters = ChapterSerializer(many=True)

    def create(self, validated_data):
        chapters_data = validated_data['chapters']
        chapters = list(self._create_or_update(chapters_data))

        # Send the component updated signal
        # (the serializer is only used from within the dashboard)
        self._send_component_updated_signal()

        return {
            'chapters': chapters
        }

    def _create_or_update(self, validated_data):
        chapter_list_serializer = self.fields['chapters']
        chapter_serializer = chapter_list_serializer.child

        chapter_ids = [chapter['id']
                       for chapter in validated_data
                       if 'id' in chapter]
        Chapter.objects \
            .filter(module_id=self.context['module_pk']) \
            .exclude(id__in=chapter_ids) \
            .delete()

        for weight, chapter_data in enumerate(validated_data):
            chapter_data['weight'] = weight
            if 'id' in chapter_data:
                instance = Chapter.objects.get(id=chapter_data['id'])
                assert instance.module_id == self.context['module_pk']
                yield chapter_serializer.update(instance, chapter_data)
            else:
                yield chapter_serializer.create(chapter_data)

    def _send_component_updated_signal(self):
        component = components.modules['document_settings']
        a4dashboard_signals.module_component_updated.send(
            sender=component.__class__,
            module=Module.objects.get(id=self.context['module_pk']),
            component=component,
            user=self.context['request'].user
        )

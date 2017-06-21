import pytest
from django.contrib.contenttypes.models import ContentType

from adhocracy4.comments import models as comments_models
from apps.documents.models import Chapter


@pytest.mark.django_db
def test_paragraph_save(paragraph):
    paragraph.text = '<script>alert("hello");</script>text'
    paragraph.save()
    assert '<script>' not in paragraph.text


@pytest.mark.django_db
def test_paragraph_knows_project(paragraph):
    assert paragraph.project == paragraph.chapter.project


@pytest.mark.django_db
def test_chapters_sorted(module, chapter_factory):
    chapter_factory(weight=2, module=module)
    chapter2 = chapter_factory(weight=1, module=module)

    chapters = Chapter.objects.filter(module=module)
    assert chapters.first() == chapter2


@pytest.mark.django_db
def test_chapter_paragraphs_sorted(chapter, paragraph_factory):
    paragraph_factory(chapter=chapter, weight=2)
    paragraph2 = paragraph_factory(chapter=chapter, weight=1)

    assert chapter.paragraphs.first() == paragraph2


@pytest.mark.django_db
def test_chapter_comments(chapter, comment_factory):
    for i in range(5):
        comment_factory(content_object=chapter)
    comment_count = comments_models.Comment.objects.all().count()
    assert comment_count == chapter.comments.count()


@pytest.mark.django_db
def test_paragraphs_comments(paragraph, comment_factory):
    for i in range(5):
        comment_factory(content_object=paragraph)
    comment_count = comments_models.Comment.objects.all().count()
    assert comment_count == paragraph.comments.count()


@pytest.mark.django_db
def test_delete_chapter(chapter, comment_factory):
    for i in range(5):
        comment_factory(content_object=chapter)

    def comments_for_chapter(chapter):
        return comments_models.Comment.objects.filter(
            object_pk=chapter.pk,
            content_type=ContentType.objects.get_for_model(chapter)
        )

    assert len(comments_for_chapter(chapter)) == 5
    chapter.delete()
    assert len(comments_for_chapter(chapter)) == 0


@pytest.mark.django_db
def test_delete_paragraph(paragraph, comment_factory):
    for i in range(5):
        comment_factory(content_object=paragraph)
    comment_count = comments_models.Comment.objects.all().count()
    assert comment_count == len(paragraph.comments.all())

    assert comment_count == 5

    paragraph.delete()
    comment_count = comments_models.Comment.objects.all().count()
    assert comment_count == 0

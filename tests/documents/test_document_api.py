import django
import pytest
from django.core.urlresolvers import reverse
from rest_framework import status

from apps.documents import models as document_models


@pytest.mark.django_db
def test_anonymous_user_can_not_retrieve_chapter_list(apiclient, module):
    url = reverse('chapters-list', kwargs={'module_pk': module.pk})
    response = apiclient.get(url, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_anonymous_user_can_not_retrieve_chapter_detail(
        apiclient, chapter, module):
    # Assert that no detail route exists
    with pytest.raises(django.core.urlresolvers.NoReverseMatch):
        url = reverse(
            'chapters-detail',
            kwargs={'module_pk': module.pk, 'pk': chapter.pk}
        )
        # if it would exist it shoud be forbidden
        response = apiclient.get(url, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_anonymous_user_can_not_create_chapter(apiclient, module):
    url = reverse('chapters-list', kwargs={'module_pk': module.pk})
    data = {
        'chapters': [
            {
                'name': 'This is a Chapter name',
                'weight': 0,
                'paragraphs': []
            }
        ]
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    count = document_models.Chapter.objects.all().count()
    assert count == 0


@pytest.mark.django_db
def test_moderator_can_create_chapter(apiclient, module):
    project = module.project
    moderator = project.moderators.first()
    apiclient.force_authenticate(user=moderator)
    url = reverse('chapters-list', kwargs={'module_pk': module.pk})
    data = {
        'chapters': [
            {
                'name': 'This is a Chapter name',
                'weight': 0,
                'paragraphs': []
            }
        ]
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    count = document_models.Chapter.objects.all().count()
    assert count == 1


@pytest.mark.django_db
def test_moderator_cannot_create_chapter_in_other_module(
        apiclient, module, project_factory):
    other_project = project_factory()
    other_moderator = other_project.moderators.first()
    apiclient.force_authenticate(user=other_moderator)
    url = reverse('chapters-list', kwargs={'module_pk': module.pk})
    data = {
        'chapters': [
            {
                'name': 'This is a Chapter name',
                'weight': 0,
                'paragraphs': []
            }
        ]
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_chapters_are_correctly_sorted(apiclient, module):
    project = module.project
    moderator = project.moderators.first()
    apiclient.force_authenticate(user=moderator)
    url = reverse('chapters-list', kwargs={'module_pk': module.pk})
    data = {
        'chapters': [
            {
                'name': 'chapter 1',
                'weight': 1000,
                'paragraphs': []
            },
            {
                'name': 'chapter 2',
                'weight': 0,
                'paragraphs': []
            }
        ]
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['chapters'][0]['name'] == 'chapter 1'
    assert response.data['chapters'][1]['name'] == 'chapter 2'


@pytest.mark.django_db
def test_paragraphs_are_correctly_sorted(apiclient, module):
    project = module.project
    moderator = project.moderators.first()
    apiclient.force_authenticate(user=moderator)
    url = reverse('chapters-list', kwargs={'module_pk': module.pk})
    data = {
        'chapters': [
            {
                'name': 'This is a Chapter name',
                'weight': 0,
                'paragraphs': [
                    {
                        'name': 'paragraph 1',
                        'text': 'text for paragraph 1',
                        'weight': 3
                    },
                    {
                        'name': 'paragraph 2',
                        'text': 'text for paragraph 2',
                        'weight': 1
                    },
                    {
                        'name': 'paragraph 3',
                        'text': 'text for paragraph 3',
                        'weight': 0
                    }

                ]
            }
        ]
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    chapter = response.data['chapters'][0]
    assert chapter['paragraphs'][0]['name'] == 'paragraph 1'
    assert chapter['paragraphs'][1]['name'] == 'paragraph 2'
    assert chapter['paragraphs'][2]['name'] == 'paragraph 3'


@pytest.mark.django_db
def test_moderator_can_delete_chapter(apiclient, module):
    project = module.project
    moderator = project.moderators.first()
    apiclient.force_authenticate(user=moderator)
    url = reverse('chapters-list', kwargs={'module_pk': module.pk})
    data = {
        'chapters': [
            {
                'name': 'chapter 1',
                'paragraphs': []
            },
            {
                'name': 'chapter 2',
                'paragraphs': []
            }
        ]
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    chapter_count = document_models.Chapter.objects.all().count()
    assert chapter_count == 2
    chapter_0_pk = response.data['chapters'][0]['id']

    data = {
        'chapters': [
            {
                'id': chapter_0_pk,
                'name': 'chapter 1',
                'paragraphs': []
            },
        ]
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    chapter_count = document_models.Chapter.objects.all().count()
    assert chapter_count == 1


@pytest.mark.django_db
def test_moderator_can_delete_paragraph(apiclient, module):
    project = module.project
    moderator = project.moderators.first()
    apiclient.force_authenticate(user=moderator)
    url = reverse('chapters-list', kwargs={'module_pk': module.pk})
    data = {
        'chapters': [
            {
                'name': 'This is a text',
                'paragraphs': [
                    {
                        'name': 'paragraph 1',
                        'text': 'text for paragraph 1',
                        'weight': 0
                    },
                    {
                        'name': 'paragraph 2',
                        'text': 'text for paragraph 2',
                        'weight': 1
                    }
                ]
            }
        ]
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    chapters = document_models.Chapter.objects.all()
    chapter_count = chapters.count()
    assert chapter_count == 1
    chapter_pk = response.data['chapters'][0]['id']
    paragraphs_count = chapters.first().paragraphs.count()
    paragraphs_all_count = document_models.Paragraph.objects.all().count()
    assert paragraphs_count == 2
    assert paragraphs_all_count == 2

    data = {
        'chapters': [
            {
                'id': chapter_pk,
                'name': 'This is a text',
                'paragraphs': [
                    {
                        'name': 'paragraph 2',
                        'text': 'text for paragraph 2',
                        'weight': 1
                    }
                ]
            }
        ]
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    paragraphs_count = chapters.first().paragraphs.count()
    paragraphs_all_count = document_models.Paragraph.objects.all().count()
    assert paragraphs_count == 1
    assert paragraphs_all_count == 1


@pytest.mark.django_db
def test_moderator_can_update_chapter(apiclient, module):
    project = module.project
    moderator = project.moderators.first()
    apiclient.force_authenticate(user=moderator)
    url = reverse('chapters-list', kwargs={'module_pk': module.pk})
    data = {
        'chapters': [
            {
                'name': 'This is a text',
                'paragraphs': []
            }
        ]
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    chapters_all_count = document_models.Chapter.objects.all().count()
    assert chapters_all_count == 1

    chapter_pk = response.data['chapters'][0]['id']
    chapter_name = document_models.Chapter.objects.get(pk=chapter_pk).name
    assert chapter_name == 'This is a text'

    data = {
        'chapters': [
            {
                'id': chapter_pk,
                'name': 'This is a text updated',
                'paragraphs': []
            }
        ]
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    chapters_all_count = document_models.Chapter.objects.all().count()
    assert chapters_all_count == 1

    chapter_name = document_models.Chapter.objects.get(pk=chapter_pk).name
    assert chapter_name == 'This is a text updated'


@pytest.mark.django_db
def test_moderator_can_update_paragraph(apiclient, module):
    project = module.project
    moderator = project.moderators.first()
    apiclient.force_authenticate(user=moderator)
    url = reverse('chapters-list', kwargs={'module_pk': module.pk})
    data = {
        'chapters': [
            {
                'name': 'This is a text',
                'paragraphs': [
                    {
                        'name': 'paragraph 1',
                        'text': 'text for paragraph 1',
                        'weight': 0
                    }
                ]
            }
        ]
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    paragraphs_all_count = document_models.Paragraph.objects.all().count()
    assert paragraphs_all_count == 1

    chapter_pk = response.data['chapters'][0]['id']
    paragraph_pk = response.data['chapters'][0]['paragraphs'][0]['id']
    paragraph_text = document_models.Paragraph.objects.get(
        pk=paragraph_pk).text
    assert paragraph_text == 'text for paragraph 1'

    data = {
        'chapters': [
            {
                'id': chapter_pk,
                'name': 'This is a text',
                'paragraphs': [
                    {
                        'id': paragraph_pk,
                        'name': 'paragraph 1',
                        'text': 'text for paragraph 1 updated',
                        'weight': 0
                    },
                ]
            }
        ]
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    paragraph_text = document_models.Paragraph.objects.get(
        pk=paragraph_pk).text
    assert paragraph_text == 'text for paragraph 1 updated'

    paragraphs_all_count = document_models.Paragraph.objects.all().count()
    assert paragraphs_all_count == 1


@pytest.mark.django_db
def test_moderator_can_update_and_create_chapter(apiclient, module):
    project = module.project
    moderator = project.moderators.first()
    apiclient.force_authenticate(user=moderator)
    url = reverse('chapters-list', kwargs={'module_pk': module.pk})
    data = {
        'chapters': [
            {
                'name': 'chapter 1',
                'paragraphs': []
            }
        ]
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    chapters_all_count = document_models.Chapter.objects.all().count()
    assert chapters_all_count == 1

    chapter_pk = response.data['chapters'][0]['id']
    chapter_name = document_models.Chapter.objects.get(pk=chapter_pk).name
    assert chapter_name == 'chapter 1'

    data = {
        'chapters': [
            {
                'id': chapter_pk,
                'name': 'chapter 1 updated',
                'paragraphs': []
            },
            {
                'name': 'chapter 2',
                'paragraphs': []
            }
        ]
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    chapters_all_count = document_models.Chapter.objects.all().count()
    assert chapters_all_count == 2

    chapter_0_name = document_models.Chapter.objects.get(pk=chapter_pk).name
    assert chapter_0_name == 'chapter 1 updated'

    paragraph_1_pk = response.data['chapters'][1]['id']
    paragraph_1_name = document_models.Chapter.objects\
        .get(pk=paragraph_1_pk).name
    assert paragraph_1_name == 'chapter 2'


@pytest.mark.django_db
def test_moderator_can_update_and_create_paragraph(apiclient, module):
    project = module.project
    moderator = project.moderators.first()
    apiclient.force_authenticate(user=moderator)
    url = reverse('chapters-list', kwargs={'module_pk': module.pk})
    data = {
        'chapters': [
            {
                'name': 'This is a text',
                'paragraphs': [
                    {
                        'name': 'paragraph 1',
                        'text': 'text for paragraph 1',
                        'weight': 0
                    },
                ]
            }
        ]
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    chapters_all_count = document_models.Chapter.objects.all().count()
    assert chapters_all_count == 1

    paragraphs_all_count = document_models.Paragraph.objects.all().count()
    assert paragraphs_all_count == 1

    chapter = response.data['chapters'][0]
    chapter_pk = chapter['id']
    paragraph_pk = chapter['paragraphs'][0]['id']
    paragraph_text = document_models.Paragraph.objects.get(
        pk=paragraph_pk).text
    assert paragraph_text == 'text for paragraph 1'

    data = {
        'chapters': [
            {
                'id': chapter_pk,
                'name': 'This is a text',
                'paragraphs': [
                    {
                        'name': 'paragraph 1',
                        'text': 'text for paragraph 1 updated',
                        'weight': 0,
                        'id': paragraph_pk
                    },
                    {
                        'name': 'paragraph 2',
                        'text': 'text for paragraph 2',
                        'weight': 2
                    }
                ]
            }
        ]
    }
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    chapter = response.data['chapters'][0]
    paragraph_0_pk = chapter['paragraphs'][0]['id']
    paragraph_0_text = document_models.Paragraph.objects.get(
        pk=paragraph_0_pk).text
    assert paragraph_0_text == 'text for paragraph 1 updated'

    paragraph_1_pk = chapter['paragraphs'][1]['id']
    paragraph_1_text = document_models.Paragraph.objects.get(
        pk=paragraph_1_pk).text
    assert paragraph_1_text == 'text for paragraph 2'

    paragraphs_all_count = document_models.Paragraph.objects.all().count()
    assert paragraphs_all_count == 2

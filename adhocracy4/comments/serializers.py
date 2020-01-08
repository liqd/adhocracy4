from django.conf import settings
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.utils import model_meta

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_profile_url = serializers.SerializerMethodField()
    is_deleted = serializers.SerializerMethodField()
    ratings = serializers.SerializerMethodField()
    is_moderator = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        read_only_fields = ('modified', 'created', 'id',
                            'user_name', 'ratings', 'content_type',
                            'object_pk', 'last_discussed',
                            'is_moderator_marked')
        exclude = ('creator', 'is_censored', 'is_removed')

    def to_representation(self, instance):
        """
        Gets the categories and adds them along with their values
        to a dictionary
        """
        ret = super().to_representation(instance)
        categories = {}
        if ret['comment_categories']:
            category_choices = getattr(settings,
                                       'A4_COMMENT_CATEGORIES', '')
            if category_choices:
                category_choices = dict((x, str(y)) for x, y
                                        in category_choices)
            category_list = ret['comment_categories'].strip('[]').split(',')
            for category in category_list:
                if category in category_choices:
                    categories[category] = category_choices[category]
                else:
                    categories[category] = category
        ret['comment_categories'] = categories
        return ret

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if 'comment_categories' in data:
            value = data.get('comment_categories')
            if value == '' or value == '[]':
                raise serializers.ValidationError({
                    'comment_categories': _('Please choose a category')
                })
        return data

    def get_user_name(self, obj):
        """
        Don't show username if comment is marked removed or censored
        """
        if(obj.is_censored or obj.is_removed):
            return _('unknown user')
        return str(obj.creator.username)

    def get_user_profile_url(self, obj):
        if obj.is_censored or obj.is_removed:
            return ''
        try:
            return obj.creator.get_absolute_url()
        except AttributeError:
            return ''

    def get_is_moderator(self, obj):
        return obj.project.has_moderator(obj.creator)

    def get_is_deleted(self, obj):
        """
        Returns true is one of the flags is set
        """
        return (obj.is_censored or obj.is_removed)

    def get_ratings(self, comment):
        """
        Gets positve and negative rating count as well as
        info on the request users rating
        """
        user = self.context['request'].user
        positive_ratings = comment.ratings.filter(value=1).count()
        negative_ratings = comment.ratings.filter(value=-1).count()

        if user.is_authenticated:
            user_rating = comment.ratings.filter(creator=user).first()
        else:
            user_rating = None

        if user_rating:
            user_rating_value = user_rating.value
            user_rating_id = user_rating.pk
        else:
            user_rating_value = None
            user_rating_id = None

        result = {
            'positive_ratings': positive_ratings,
            'negative_ratings': negative_ratings,
            'current_user_rating_value': user_rating_value,
            'current_user_rating_id': user_rating_id
        }

        return result


class ThreadSerializer(CommentSerializer):
    """
    Serializes a comment including child comment (replies).
    """
    child_comments = CommentSerializer(many=True, read_only=True)


class CommentModerateSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        """
        Create a dictionary form categories.

        Gets the categories and adds them along with their values
        to a dictionary.
        """
        ret = super().to_representation(instance)
        categories = {}
        if ret['comment_categories']:
            category_choices = getattr(settings,
                                       'A4_COMMENT_CATEGORIES', '')
            if category_choices:
                category_choices = dict((x, str(y)) for x, y
                                        in category_choices)
            category_list = ret['comment_categories'].strip('[]').split(',')
            for category in category_list:
                if category in category_choices:
                    categories[category] = category_choices[category]
                else:
                    categories[category] = category
        ret['comment_categories'] = categories
        return ret

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if 'comment_categories' in data:
            value = data.get('comment_categories')
            if value == '' or value == '[]':
                raise serializers.ValidationError({
                    'comment_categories': _('Please choose a category')
                })
        return data

    def update(self, instance, validated_data):
        serializers.raise_errors_on_nested_writes('update', self,
                                                  validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save(ignore_modified=True)

        return instance

    class Meta:
        model = Comment
        fields = ('is_moderator_marked', 'modified', 'created', 'id',
                  'content_type', 'object_pk', 'last_discussed', 'comment',
                  'comment_categories')
        read_only_fields = ('modified', 'created', 'id', 'content_type',
                            'object_pk', 'last_discussed', 'comment',
                            'comment_categories')

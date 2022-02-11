from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from easy_thumbnails.files import get_thumbnailer
from rest_framework import serializers

from adhocracy4.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Default Serializer for the comments."""

    user_name = serializers.SerializerMethodField()
    user_profile_url = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    is_deleted = serializers.SerializerMethodField()
    ratings = serializers.SerializerMethodField()
    is_moderator = serializers.SerializerMethodField()
    comment_content_type = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        read_only_fields = ('modified', 'created', 'id',
                            'user_name', 'user_image', 'ratings',
                            'content_type', 'object_pk',
                            'comment_content_type')
        exclude = ('creator',)

    def to_representation(self, instance):
        """
        Create category-dict, don't show blocked comments, add permissions.

        Gets the categories and adds them along with their values
        to a dictionary. Do return empty dict when comment is_blocked.
        Does return empty string as comment text when comment is_blocked.
        """
        ret = super().to_representation(instance)
        categories = {}
        if ret['comment_categories'] and not instance.is_blocked:
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
        if instance.is_blocked:
            ret['comment'] = ''

        request = self.context.get('request')
        ret['is_users_own_comment'] = False
        ret['authenticated_user_pk'] = None

        ret['has_viewing_permission'] = False
        ret['has_rating_permission'] = False
        ret['has_changing_permission'] = False
        ret['has_deleting_permission'] = False
        ret['has_moderating_permission'] = False
        if request and hasattr(request, 'user'):
            user = request.user
            ret['is_users_own_comment'] = (user.pk == instance.creator.pk)
            ret['authenticated_user_pk'] = user.pk

            ret['has_viewing_permission'] = user.has_perm(
                'a4comments.view_comment', instance
            )
            ret['has_rating_permission'] = user.has_perm(
                'a4comments.rate_comment', instance
            )
            ret['has_changing_permission'] = user.has_perm(
                'a4comments.change_comment', instance
            )
            ret['has_deleting_permission'] = user.has_perm(
                'a4comments.delete_comment', instance
            )
            ret['has_moderating_permission'] = user.has_perm(
                'a4comments.moderate_comment', instance
            )

        return ret

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if 'comment_categories' in data:
            value = data.get('comment_categories')
            if value == '' or value == '[]':
                raise serializers.ValidationError({
                    'comment_categories': _('Please choose one or more '
                                            'categories.')
                })
        return data

    def get_user_profile_url(self, obj):
        if obj.is_censored or obj.is_removed or obj.is_blocked:
            return ''
        try:
            return obj.creator.get_absolute_url()
        except AttributeError:
            return ''

    def get_user_name(self, obj):
        """Don't show username if comment is marked removed or censored."""
        if obj.is_censored or obj.is_removed or obj.is_blocked:
            return _('unknown user')
        return obj.creator.get_short_name()

    def get_user_image_fallback(self, obj):
        """Load small thumbnail images for default user images."""
        if obj.is_censored or obj.is_removed or obj.is_blocked:
            return None
        try:
            if obj.creator.avatar_fallback:
                return obj.creator.avatar_fallback
        except AttributeError:
            pass
        return None

    def get_user_image(self, obj):
        """Load small thumbnail images for user images."""
        if obj.is_censored or obj.is_removed or obj.is_blocked:
            return None
        try:
            if obj.creator.avatar:
                avatar = get_thumbnailer(obj.creator.avatar)['avatar']
                return avatar.url
        except AttributeError:
            pass
        return self.get_user_image_fallback(obj)

    def get_is_moderator(self, obj):
        return obj.project.has_moderator(obj.creator)

    def get_is_deleted(self, obj):
        """Return true if one of the flags is set."""
        return obj.is_censored or obj.is_removed or obj.is_blocked

    def get_ratings(self, comment):
        """
        Get positive and negative rating count.

        As well as info on the request users rating
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

    def get_comment_content_type(self, comment):
        return ContentType.objects.get_for_model(Comment).pk


class CommentListSerializer(CommentSerializer):
    """Serializer for the comments to be used when viewed as list."""


class ThreadSerializer(CommentSerializer):
    """Serializes a comment including child comment (replies)."""

    child_comments = CommentSerializer(many=True, read_only=True)


class ThreadListSerializer(CommentListSerializer):
    """
    Serializes comments when viewed.

    As list including child comment (replies).
    """

    child_comments = CommentListSerializer(many=True, read_only=True)

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from easy_thumbnails.files import get_thumbnailer
from rest_framework import serializers

from adhocracy4.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Default Serializer for the comments."""

    user_name = serializers.SerializerMethodField()
    user_pk = serializers.SerializerMethodField()
    user_profile_url = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    is_deleted = serializers.SerializerMethodField()
    ratings = serializers.SerializerMethodField()
    is_moderator = serializers.SerializerMethodField()
    comment_content_type = serializers.SerializerMethodField()
    has_rating_permission = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        read_only_fields = ('modified', 'created', 'id',
                            'user_name', 'user_pk', 'user_image',
                            'user_image_fallback', 'ratings',
                            'content_type', 'object_pk',
                            'comment_content_type', 'has_rating_permission')
        exclude = ('creator',)

    def to_representation(self, instance):
        """
        Create a dictionary form categories and don't show blocked comments.

        Gets the categories and adds them along with their values
        to a dictionary.
        Also gets the comments and blocks their content
        from being shown if they are set to blocked.
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
        is_blocked = ret.get('is_blocked')
        if is_blocked:
            ret['comment'] = ''
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

    def get_user_pk(self, obj):
        if (obj.is_censored or obj.is_removed):
            return -1
        return str(obj.creator.id)

    def get_user_profile_url(self, obj):
        if obj.is_censored or obj.is_removed:
            return ''
        try:
            return obj.creator.get_absolute_url()
        except AttributeError:
            return ''

    def get_user_name(self, obj):
        """Don't show username if comment is marked removed or censored."""
        if(obj.is_censored or obj.is_removed):
            return _('unknown user')
        return obj.creator.get_short_name()

    def get_user_image_fallback(self, obj):
        """Load small thumbnail images for default user images."""
        if(obj.is_censored or obj.is_removed):
            return None
        try:
            if obj.creator.avatar_fallback:
                return obj.creator.avatar_fallback
        except AttributeError:
            pass
        return None

    def get_user_image(self, obj):
        """Load small thumbnail images for user images."""
        if(obj.is_censored or obj.is_removed):
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
        return (obj.is_censored or obj.is_removed)

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

    # used in zt-app, where we can't pass props through template tags
    # FIXME: this should replace comments_contenttype passed in template tag
    def get_comment_content_type(self, comment):
        return ContentType.objects.get_for_model(Comment).pk

    def get_has_rating_permission(self, comment):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            return user.has_perm('a4comments.rate_comment', comment)
        return False


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

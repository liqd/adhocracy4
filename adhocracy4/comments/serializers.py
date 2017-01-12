from django.utils.translation import ugettext as _
from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    is_deleted = serializers.SerializerMethodField()
    ratings = serializers.SerializerMethodField()
    is_moderator = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        read_only_fields = ('modified', 'created', 'id',
                            'user_name', 'ratings')
        exclude = ('creator', 'is_censored', 'is_removed')

    def get_user_name(self, obj):
        """
        Don't show username if comment is marked removed or censored
        """
        if(obj.is_censored or obj.is_removed):
            return _('unknown user')
        return str(obj.creator.username)

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

        if user.is_authenticated():
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

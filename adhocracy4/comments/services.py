from .models import Comment


def delete_comments(contenttype, pk):
    comments = Comment.objects.all().filter(
        content_type=contenttype, object_pk=pk)
    for comment in comments:
        comment.delete()

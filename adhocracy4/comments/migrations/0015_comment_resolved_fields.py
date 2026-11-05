from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("a4comments", "0014_rename_comment_content_type_object_pk_a4comments__content_ff606b_idx"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    "ALTER TABLE a4comments_comment ADD COLUMN "
                    "is_resolved boolean NOT NULL DEFAULT FALSE;",
                    reverse_sql="ALTER TABLE a4comments_comment DROP COLUMN is_resolved;",
                ),
                migrations.RunSQL(
                    "ALTER TABLE a4comments_comment ADD COLUMN "
                    "resolved_at timestamp with time zone NULL;",
                    reverse_sql="ALTER TABLE a4comments_comment DROP COLUMN resolved_at;",
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name="comment",
                    name="is_resolved",
                    field=models.BooleanField(default=False),
                ),
                migrations.AddField(
                    model_name="comment",
                    name="resolved_at",
                    field=models.DateTimeField(blank=True, null=True),
                ),
            ],
        ),
    ]

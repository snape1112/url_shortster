from django.db import models
import uuid
import jsonfield

NULL_AND_BLANK = {'null': True, 'blank': True}

class TagHistory(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="The unique identifier of the instance this object belongs to. Mandatory, unless a new instance to create is given."
    )

    name = models.CharField(
        max_length=50,
        **NULL_AND_BLANK,
        verbose_name="Name",
        help_text="Name of tag",
    )

# Create your models here.
class BlogPost(models.Model):
    id = models.IntegerField(
        primary_key=True,
        default=0,
        verbose_name="ID",
        help_text="The id of post",
    )

    author = models.CharField(
        max_length=50,
        **NULL_AND_BLANK,
        verbose_name="Author",
        help_text="Who wrote this post",
    )

    authorId = models.IntegerField(
        **NULL_AND_BLANK,
        default=0,
        verbose_name="Author ID",
        help_text="ID of author",
    )

    likes = models.IntegerField(
        **NULL_AND_BLANK,
        default=0,
        verbose_name="Likes",
        help_text="Number of likes",
    )

    popularity = models.DecimalField(
        **NULL_AND_BLANK,
        default=0,
        max_digits=18,
        decimal_places=2,
        verbose_name="Popularity",
        help_text="Popularity of post",
    )

    reads = models.IntegerField(
        **NULL_AND_BLANK,
        default=0,
        verbose_name="Reads",
        help_text="Number of reads",
    )

    tags = jsonfield.JSONField(
        **NULL_AND_BLANK,
        verbose_name="Tags",
        help_text="""List of tags. Ex: ["tech", "health]""",
    )

    class Meta:
        verbose_name = "BlogPost"
        verbose_name_plural = "BlogPosts"
    
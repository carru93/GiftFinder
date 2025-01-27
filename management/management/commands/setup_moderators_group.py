from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from forum.models import Comment, Post


class Command(BaseCommand):
    help = 'Create the "Moderators" group and assign permissions to delete posts and comments.'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Moderators")
        if created:
            self.stdout.write(
                self.style.SUCCESS('Group "Moderators" created successfully.')
            )
        else:
            self.stdout.write('The group "Moderators" already exists.')

        post_ct = ContentType.objects.get_for_model(Post)
        comment_ct = ContentType.objects.get_for_model(Comment)

        delete_post_perm = Permission.objects.get(
            codename="delete_post", content_type=post_ct
        )
        delete_comment_perm = Permission.objects.get(
            codename="delete_comment", content_type=comment_ct
        )

        group.permissions.add(delete_post_perm, delete_comment_perm)

        self.stdout.write(
            self.style.SUCCESS('Delete permissions assigned to the "Moderators" group.')
        )

# coding=utf-8
from django.core.management.base import BaseCommand

from user_map.app_settings import ROLES
from user_map.models.role import Role


class Command(BaseCommand):
    help = 'Update the roles in the database'

    def handle(self, *args, **options):
        """This command should be called after changing the roles in
        settings in the case that you have called migrate (roles table is
        already filled with some data)

        Bear in mind that you should keep the ids the same and just change
        the name or the badge path. And this command will only update the role
        table, not the usermap table that uses the role table.

        So, adding roles is fine (as long as the new ids are unique). Removing
        roles has no effect (it will not remove the row in the table). Well, it
        could give you problems as it means that some of the users might not
        have valid roles defined in the role table.

        How to use this:
            python manage.py update_roles
        """
        for new_role in ROLES:
            try:
                role = Role.objects.get(pk=new_role['id'])
                old_name = role.name
                old_badge = role.badge
                role.name = new_role['name']
                role.badge = new_role['badge']
                role.save()
                self.stdout.write(
                    'Role (%s, %s, %s) has been updated to (%s, %s, %s)' % (
                        role.id, old_name, old_badge,
                        role.id, role.name, role.badge
                    )
                )
            except Role.DoesNotExist:
                # It means a new role
                role = Role.objects.create(
                    id=new_role['id'],
                    name=new_role['name'],
                    badge=new_role['badge']
                )
                self.stdout.write(
                    'New Role (%s, %s, %s) has been added' % (
                        role.id, role.name, role.badge,
                    )
                )

        self.stdout.write('> The operation update_role is run successfully.')

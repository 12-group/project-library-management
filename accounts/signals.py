# from django.db.models.signals import post_save
# from django.contrib.auth.models import User


# from .models import *

# def reader_profile(sender, instance, created, **kwargs):
# 	if created:
		
# 		Reader.objects.create(
# 			user=instance,
# 			name=instance.username,
# 		)
# 		print('Profile created!')

# post_save.connect(reader_profile, sender=User)

# from django.apps import AppConfig
# from django.db.models.signals import post_migrate
from .models import *

# class AccountsConfig(AppConfig):
#     name = 'accounts'

#     def ready(self):
#         from .signals import populate_models
#         post_migrate.connect(populate_models, sender=self)

def populate_models(sender, **kwargs):
    '''
    Khoi tao cac group
    Khoi tao user manager
    '''
    from django.contrib.auth.models import User
    from django.contrib.auth.models import Group

    # khoi tao cac group
    staff_group, staff_group_created = Group.objects.get_or_create(name='staff')
    Group.objects.get_or_create(name='reader')
    Group.objects.get_or_create(name='librarian')
    Group.objects.get_or_create(name='storekeeper')
    Group.objects.get_or_create(name='cashier')
    manager_group, manager_group_created = Group.objects.get_or_create(name='manager')

    '''
    Khoi tao user, them vao group manager
        user:
            username = manager
            email = ''
            password = DEFAULT_PASSWORD
    '''

    # tim user co username = manager
    user, user_created = User.objects.get_or_create(
        username='manager',
        defaults={
            'email': '', 
            }
    )
    if user_created:
        user.set_password(DEFAULT_PASSWORD)
        user.save()

    
    if not user.groups.filter(name='manager').exists():
        # them user vao group manager
        user.groups.add(manager_group)

    if not user.groups.filter(name='staff').exists():
    # them user vao group staff
        user.groups.add(staff_group)

    # tao Staff
    Staff.objects.get_or_create(
        user=user,
        defaults={
            'name':user.username,
            'position':'Manager',
            'service':'Manager department'
        }
    )


    


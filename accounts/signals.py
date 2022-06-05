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
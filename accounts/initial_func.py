from . import models

def pk_gen():
	readers = models.Reader.objects.all()
	pk = 0
	for reader in readers:
		pk += 1
		if reader.pk != 'DG{}'.format(str(pk).zfill(6)):
			print(reader.pk)
			return 'DG{}'.format(str(pk).zfill(6))
	pk += 1
	return 'DG{}'.format(str(pk).zfill(6))


def staff_pk_gen():
	staffs = models.Staff.objects.all()
	pk = 0
	for staff in staffs:
		pk += 1
		if staff.pk != 'NV{}'.format(str(pk).zfill(6)):
			print(staff.pk)
			return 'NV{}'.format(str(pk).zfill(6))
	pk += 1
	return 'NV{}'.format(str(pk).zfill(6))

def username_gen():
	
	users = models.User.objects.all()

	count = 1
	gen_username = 'staff{}'.format(count)

	usernames = [user.username for user in users]

	while gen_username in usernames:
		count += 1
		gen_username = 'staff{}'.format(count)

	return gen_username

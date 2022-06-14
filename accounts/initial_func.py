from . import models

def pk_gen():

	readers = models.Reader.objects.all()
	readers_pk = [reader.rId for reader in readers]
	pk = 1
	result = 'DG{}'.format(str(pk).zfill(6))

	while result in readers_pk:
		pk += 1
		result = 'DG{}'.format(str(pk).zfill(6))

	return result


def staff_pk_gen():
	staffs = models.Staff.objects.all()
	staffs_pk = [staff.sId for staff in staffs]
	pk = 1
	result = 'NV{}'.format(str(pk).zfill(6))

	while result in staffs_pk:
		pk += 1
		result = 'NV{}'.format(str(pk).zfill(6))
	return result
	 



def username_gen():
	
	users = models.User.objects.all()

	count = 1
	gen_username = 'staff{}'.format(count)

	usernames = [user.username for user in users]

	while gen_username in usernames:
		count += 1
		gen_username = 'staff{}'.format(count)

	return gen_username

def book_pk_gen():
	
	books = models.Book.objects.all()
	pk = 0
	for book in books:
		pk += 1
		if book.pk != 'S{}'.format(str(pk).zfill(6)):
			print(book.pk)
			return 'S{}'.format(str(pk).zfill(6))
	pk += 1
	return 'S{}'.format(str(pk).zfill(6))

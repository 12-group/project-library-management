from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout

def is_in_group(check_group, groups):
    if check_group in [group.name for group in groups]:
        return True
    return False

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			groups = None
			if request.user.groups.exists():
				groups = request.user.groups.all()
			if is_in_group('staff', groups):
				pass
			# if group in allowed_roles:
			# 	return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('Bạn không có quyền để xem trang này')
		return wrapper_func
	return decorator

def redirect_home_view(view_func):
	def wrapper_func(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			#group = request.user.groups.all()[0].name
			groups = request.user.groups.all()
			group = [g.name for g in groups]
		if 'reader' in group:
			return view_func(request, *args, **kwargs)

		elif 'librarian' in group:
			return redirect('librarian') 

		elif 'stockkeeper' in group:
			return redirect('list_book')

		elif 'cashier' in group:
			return redirect('receipt_list')

		elif 'manager' in group:
			return redirect('manager_dashboard')

		if not group:
			logout(request)
			return redirect('login')
	return wrapper_func
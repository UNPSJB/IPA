from django.conf import settings
from django.contrib.auth.hashers import check_password
from apps.users.models import Usuario
from django.contrib.auth import authenticate as django_auth

class UserBackend(object):
	def authenticate(self, request, username=None, password=None):
		username = self.sanitizate(username)
		user = django_auth(request, username=username, password=password)
		if user is None:
			try :
				userObject = Usuario.objects.get(email=username)
			except Usuario.DoesNotExist:
				print('usuario no existe')
				return None
			user = django_auth(request, username=userObject.username, password=password)
		return user

	def sanitizate(self, username):
		return username.lower()
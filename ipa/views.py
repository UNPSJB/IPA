from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, PasswordResetView 
from django.shortcuts import render, redirect
from apps.users.backend import UserBackend

# Create your views here.
class Login(LoginView):
	template_name = 'login/login.html'
	success_url = reverse_lazy('index')

	def post(self, request, *args, **kwargs):		
		# Se toman user y password del formulario
		username = request.POST['username']
		password = request.POST['password']

		# Se intenta autenticar por username
		userBackend = UserBackend()
		user = userBackend.authenticate(request, username=username, password=password)
						
		if user is not None:
			login(request, user)
			return redirect(self.success_url)
		return render(request, self.template_name, {'message_error': 'Usuario o contraseña incorrectos'})

class PasswordReset(PasswordResetView):
	failure_url = reverse_lazy('login')

	def form_invalid(self, form):
		"""If the form is invalid, render the invalid form."""
		return self.redirect(self.failure_url)


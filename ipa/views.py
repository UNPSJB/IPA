from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

# Create your views here.
class Login(LoginView):
	template_name = 'login/login.html'
	success_url = reverse_lazy('index')

	def post(self, request, *args, **kwargs):		
		# Se toman user y password del formulario
		username = request.POST['username']
		password = request.POST['password']

		# Se intenta autenticar por username
		user = authenticate(request, username=username, password=password)

		# Si no se pudo
		if user is None:
			# Se intenta autenticar por email
			user = authenticate(request, email=username, password=password) 
			
		if user is not None:
			login(request, user)
			return redirect(self.success_url)
		return render(request, self.template_name, {'message_error': 'Usuario o contraseña incorrectos'})
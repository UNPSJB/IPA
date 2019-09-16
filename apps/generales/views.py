from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

# Create your views here.
class GenericAltaView(CreateView):
	botones = dict()

	def form_valid(self,form):
		self.object = form.save()
		if self.object != None:
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form, message = self.message_error))

	def post(self, request, *args, **kwargs):
		super(GenericAltaView, self).post(request,*args,**kwargs)
		if 'cargarOtro' in request.POST:
			return redirect(self.cargar_otro_url)
		return redirect(self.success_url)

	def get_context_data(self, **kwargs):
		context = super(GenericAltaView, self).get_context_data(**kwargs)
		context['botones'] = self.botones
		return context

class GenericModificacionView(UpdateView):
	template_name = 'forms.html'

	def get_context_data(self, **kwargs):
		context = super(GenericModificacionView, self).get_context_data(**kwargs)
		context['nombreForm'] = self.nombre_form
		context['botones'] = self.botones
		return context
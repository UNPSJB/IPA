from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView


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
			cargarOtroValue = request.POST.get('cargarOtro', '')
			form_url = self.cargar_otro_url
			if cargarOtroValue != '':
				form_url = form_url + f'?return_path={cargarOtroValue}'		
			return redirect(form_url)
		return_path = request.POST.get('guardar', self.success_url)
		return redirect(return_path)

	def get_context_data(self, **kwargs):
		context = super(GenericAltaView, self).get_context_data(**kwargs)
		context['return_path'] = self.request.GET.get('return_path', self.success_url)
		context['botones'] = self.botones
		return context

class GenericModificacionView(UpdateView):


	def get_context_data(self, **kwargs):
		context = super(GenericModificacionView, self).get_context_data(**kwargs)
		context['nombreForm'] = self.nombre_form
		context['botones'] = self.botones
		return context

class GenericEliminarView(DeleteView):
	def delete(self, request, *args, **kwargs):
		try:
			self.object = self.get_object()
			self.object.delete()

			return JsonResponse({
				"success": True
			})
		except Error as e:
			return JsonResponse({
				"success": False,
				"message": e.value()
			})

######################################################################
class GenericListadoView(SingleTableMixin, FilterView):
	pass
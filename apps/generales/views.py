from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView,DetailView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib import messages


class GenericAltaView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
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

	def handle_no_permission(self):
		messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
		return redirect(self.redirect_url)

	def get_context_data(self, **kwargs):
		context = super(GenericAltaView, self).get_context_data(**kwargs)
		context['return_path'] = self.request.GET.get('return_path', self.success_url)
		context['return_label'] = self.request.GET.get('return_label')
		context['botones'] = self.botones
		return context

class GenericDetalleView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
	def handle_no_permission(self):
		messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
		return redirect(self.redirect_url)

class GenericModificacionView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):

	def handle_no_permission(self):
		messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
		return redirect(self.redirect_url)

class GenericEliminarView(LoginRequiredMixin,DeleteView):
	def delete(self, request, *args, **kwargs):
		if request.user.has_perm(self.permission_required):
			try:
				self.object = self.get_object()
				self.object.delete()

				return JsonResponse({
					"success": True
				})
			except Error as e:
				return JsonResponse({
					"success": False,
					"message": ('error','Este documento no se puede eliminar')
				})
		else:
			return JsonResponse({
					"success": False,
					"message": ('permiso','No posee los permisos necesarios para realizar esta operación')
			})
	
	def handle_no_permission(self):
		messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
		return redirect(self.redirect_url)

######################################################################
class GenericListadoView(ExportMixin, SingleTableMixin, LoginRequiredMixin,PermissionRequiredMixin,FilterView):
	def handle_no_permission(self):
		messages.error(self.request, 'No posee los permisos necesarios para realizar esta operación')
		return redirect(self.redirect_url)
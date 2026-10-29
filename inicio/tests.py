import tempfile
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from usuarios.models import Establecimiento, Usuario

# Create your tests here.
@override_settings(
	EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
	DEFAULT_FROM_EMAIL='BeyondGo <test@example.com>',
)
class SolicitudesMiembroTests(TestCase):
	def setUp(self):
		self.media_directory = tempfile.TemporaryDirectory()
		self.addCleanup(self.media_directory.cleanup)
		self.media_settings = override_settings(MEDIA_ROOT=self.media_directory.name)
		self.media_settings.enable()
		self.addCleanup(self.media_settings.disable)
		self.administrador = Usuario.objects.create_user(
			email='admin@example.com',
			password=None,
			first_name='Admin',
			telefono='+573001234567',
			rol='ADMIN',
		)

	def test_formulario_crea_solicitud_pendiente_aunque_falten_archivos(self):
		response = self.client.post(reverse('hazte_miembro'), {
			'nombre_establecimiento': 'Hotel de prueba',
			'tipo_establecimiento': 'Hotel',
			'nombre_propietario': 'María Elena',
			'email_contacto': 'miembro@example.com',
			'telefono': '+573001234568',
			'direccion': 'Carrera 1 # 2-3',
			'ciudad': 'Aquitania',
			'descripcion': 'Descripción de prueba',
		})

		self.assertRedirects(response, reverse('hazte_miembro'))
		usuario = Usuario.objects.get(email='miembro@example.com')
		solicitud = Establecimiento.objects.get(usuario=usuario)
		self.assertFalse(usuario.is_active)
		self.assertEqual(solicitud.estado_revision, 'pendiente')
		self.assertFalse(solicitud.rtn)

	def test_aprobacion_activa_cuenta_y_envia_correo_con_enlace_de_clave(self):
		solicitud = self._crear_solicitud_con_documentos()
		self.client.force_login(self.administrador)

		response = self.client.post(reverse('solicitudes_miembros'), {
			'establecimiento_id': solicitud.pk,
			'accion': 'aprobar',
		})

		solicitud.refresh_from_db()
		solicitud.usuario.refresh_from_db()
		self.assertRedirects(response, reverse('solicitudes_miembros') + '?estado=aprobada', fetch_redirect_response=False)
		self.assertEqual(solicitud.estado_revision, 'aprobada')
		self.assertTrue(solicitud.is_active)
		self.assertTrue(solicitud.usuario.is_active)
		self.assertEqual(len(mail.outbox), 1)
		self.assertIn(reverse('password_reset'), mail.outbox[0].body)

	def test_modal_muestra_datos_y_archivos_de_la_solicitud(self):
		solicitud = self._crear_solicitud_con_documentos()
		self.client.force_login(self.administrador)

		response = self.client.get(reverse('solicitudes_miembros'), {
			'estado': 'pendiente',
			'establecimiento': solicitud.pk,
		})

		self.assertContains(response, 'Hotel de prueba')
		self.assertContains(response, 'rnt.pdf')
		self.assertContains(response, 'camara.pdf')

	def test_solicitar_informacion_guarda_mensaje_y_notifica(self):
		solicitud = self._crear_solicitud_con_documentos()
		self.client.force_login(self.administrador)

		response = self.client.post(reverse('solicitudes_miembros'), {
			'establecimiento_id': solicitud.pk,
			'accion': 'solicitar_informacion',
			'observacion': 'Adjunta el certificado sanitario vigente.',
		})

		solicitud.refresh_from_db()
		self.assertRedirects(response, reverse('solicitudes_miembros') + '?estado=informacion', fetch_redirect_response=False)
		self.assertEqual(solicitud.estado_revision, 'informacion')
		self.assertIn('certificado sanitario', solicitud.observacion_revision)
		self.assertEqual(len(mail.outbox), 1)
		self.assertIn(solicitud.observacion_revision, mail.outbox[0].body)

	def test_rechazo_sin_motivo_no_cambia_estado_ni_envia_correo(self):
		solicitud = self._crear_solicitud_con_documentos()
		self.client.force_login(self.administrador)

		self.client.post(reverse('solicitudes_miembros'), {
			'establecimiento_id': solicitud.pk,
			'accion': 'rechazar',
		})

		solicitud.refresh_from_db()
		self.assertEqual(solicitud.estado_revision, 'pendiente')
		self.assertFalse(mail.outbox)

	def test_rechazo_con_motivo_guarda_estado_y_envia_correo(self):
		solicitud = self._crear_solicitud_con_documentos()
		self.client.force_login(self.administrador)

		self.client.post(reverse('solicitudes_miembros'), {
			'establecimiento_id': solicitud.pk,
			'accion': 'rechazar',
			'observacion': 'El registro comercial no está vigente.',
		})

		solicitud.refresh_from_db()
		self.assertEqual(solicitud.estado_revision, 'rechazada')
		self.assertFalse(solicitud.usuario.is_active)
		self.assertEqual(len(mail.outbox), 1)
		self.assertIn(solicitud.observacion_revision, mail.outbox[0].body)

	def test_fallo_de_correo_revierte_cambio_de_estado(self):
		solicitud = self._crear_solicitud_con_documentos()
		self.client.force_login(self.administrador)

		with patch('admin_panel.views.EmailMultiAlternatives.send', side_effect=OSError('SMTP unavailable')):
			self.client.post(reverse('solicitudes_miembros'), {
				'establecimiento_id': solicitud.pk,
				'accion': 'aprobar',
			})

		solicitud.refresh_from_db()
		solicitud.usuario.refresh_from_db()
		self.assertEqual(solicitud.estado_revision, 'pendiente')
		self.assertFalse(solicitud.usuario.is_active)

	def test_aprobacion_no_permite_documentacion_incompleta(self):
		solicitud = self._crear_solicitud_con_documentos()
		solicitud.camara_comercio = ''
		solicitud.save(update_fields=['camara_comercio'])
		self.client.force_login(self.administrador)

		self.client.post(reverse('solicitudes_miembros'), {
			'establecimiento_id': solicitud.pk,
			'accion': 'aprobar',
		})

		solicitud.refresh_from_db()
		self.assertEqual(solicitud.estado_revision, 'pendiente')
		self.assertFalse(mail.outbox)

	def _crear_solicitud_con_documentos(self):
		usuario = Usuario.objects.create_user(
			email='miembro@example.com',
			password=None,
			first_name='Miembro',
			telefono='+573001234568',
			rol='ADMIN_H',
			is_active=False,
		)
		archivo_rnt = SimpleUploadedFile('rnt.pdf', b'RNT')
		archivo_sanidad = SimpleUploadedFile('sanidad.pdf', b'Sanidad')
		archivo_camara = SimpleUploadedFile('camara.pdf', b'Camara')
		return Establecimiento.objects.create(
			usuario=usuario,
			nombre='Hotel de prueba',
			tipo='Hotel',
			direccion='Carrera 1 # 2-3',
			ciudad='Aquitania',
			rtn=archivo_rnt,
			licencia_sanitaria=archivo_sanidad,
			camara_comercio=archivo_camara,
			is_active=False,
		)

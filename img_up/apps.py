from django.apps import AppConfig


class ImgUpConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'img_up'

	def ready(self):
		import img_up.signals
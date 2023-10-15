from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import ThumbnailSize, CustomUser
from .models import Tier


@admin.register(ThumbnailSize)
class ThumbnailSizeAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'width', 'height')


@admin.register(Tier)
class TierAdmin(admin.ModelAdmin):
	list_display = ('name', 'supports_expiring_link', 'supports_original_link', 'display_thumbnail_sizes')
	list_filter = ('supports_expiring_link', 'supports_original_link')
	search_fields = ('name',)

	def display_thumbnail_sizes(self, obj):
		return ", ".join([str(ts) for ts in obj.thumbnail_size.all()])

	display_thumbnail_sizes.short_description = 'Thumbnail Sizes'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
	form = CustomUserChangeForm
	add_form = CustomUserCreationForm
	list_display = ('username', 'email', 'tier', 'is_staff', 'is_superuser')
	list_filter = ('tier', 'is_staff', 'is_superuser')
	fieldsets = (
		(None, {'fields': ('username', 'email', 'password')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		('Tier', {'fields': ('tier',)}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'email', 'password1', 'password2', 'tier')}
		 ),
	)
	search_fields = ('username', 'email')
	ordering = ('username',)

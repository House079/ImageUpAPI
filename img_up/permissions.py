from rest_framework.permissions import BasePermission


class IsAdminOrAllowed(BasePermission):

	def has_permission(self, request, view):
		return request.user.is_superuser or (request.user.is_authenticated
		                                     and
		                                     request.user.tier.supports_expiring_link is True
		                                     )

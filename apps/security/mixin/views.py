from django.shortcuts import redirect


class PermissionsRequiredMixin(object):
    required_permissions = ()
    user_check_failure_path = None

    def permission_failed(self, request, *args, **kwargs):
        return redirect(self.user_check_failure_path)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perms(self.required_permissions):
            return self.permission_failed(request, *args, **kwargs)

        return super(PermissionsRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class GroupsRequiredMixin(object):
    required_groups = ()
    user_check_failure_path = None

    def group_failed(self, request, *args, **kwargs):
        return redirect(self.user_check_failure_path)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(
                name__in=self.required_groups).exists():
            return self.group_failed(request, *args, **kwargs)

        return super(GroupsRequiredMixin, self).dispatch(
            request, *args, **kwargs)

from django.urls.base import reverse
from django.http import Http404
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import (LoginRequiredMixin)
from apps.budget import models
from .forms import SubcategoryForm


class SettingCategory(LoginRequiredMixin, ListView):
    template_name = "setting_category.html"
    model = models.Category

    def get_queryset(self):
        queryset = self.model.objects.all_my_categories(self.request.user)
        return queryset


class SettingSubCategoryAdd(LoginRequiredMixin, CreateView):
    template_name = "setting_subcategory_add.html"
    model = models.SubCategory
    form_class = SubcategoryForm

    def get_context_data(self, **kwargs):
        context = super(SettingSubCategoryAdd, self).get_context_data(**kwargs)
        context['category'] = self.get_category()
        # context['form'].fields['category'].value = category.pk
        return context

    def form_valid(self, form):
        form.save()
        return super(SettingSubCategoryAdd, self).form_valid(form)

    def get_initial(self):
        return {'category': self.get_category()}

    def get_category(self):
        category = models.Category.objects.get(
            pk=int(self.kwargs.get('category_pk')))
        return category

    def get_success_url(self):
        return reverse('budget:setting_category')


class SettingSubCategoryUpdate(LoginRequiredMixin, UpdateView):
    template_name = "setting_subcategory_update.html"
    model = models.SubCategory
    form_class = SubcategoryForm

    def get_success_url(self):
        return reverse('budget:setting_category')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(SettingSubCategoryUpdate, self).get_object()
        if not obj.category.user_insert == self.request.user:
            raise Http404
        return obj


class SettingSubCategoryDelete(LoginRequiredMixin, DeleteView):
    template_name = "setting_subcategory_delete.html"
    model = models.SubCategory
    form_class = SubcategoryForm

    def get_success_url(self):
        return reverse('budget:setting_category')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(SettingSubCategoryDelete, self).get_object()
        if not obj.category.user_insert == self.request.user:
            raise Http404
        return obj

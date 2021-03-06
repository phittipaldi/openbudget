from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.http import Http404
from django.views.generic import FormView, RedirectView, UpdateView, DeleteView
from django.http.response import HttpResponseForbidden
from .forms import ImportTransactionForm, UploadedTransactionForm
from . import models
from django.urls import reverse


class DeleteUploadTransaction(LoginRequiredMixin, DeleteView):
    template_name = 'upload_transaction_delete.html'
    model = models.TransactionUploaded

    def get_success_url(self):
        return reverse('budget:accounts_sync_file',
                       kwargs={'account_pk': self.object.account.pk})

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DeleteUploadTransaction, self).get_object()
        if not obj.account.owners.filter(username__in=[
                                         self.request.user]).count():
            raise Http404
        return obj


class UpdateUploadTransaction(LoginRequiredMixin, UpdateView):
    template_name = 'modals/content_upload_transaction.html'
    form_class = UploadedTransactionForm
    model = models.TransactionUploaded

    def __init__(self, *args, **kwargs):
        super(UpdateUploadTransaction, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(
            UpdateUploadTransaction, self).get_context_data(**kwargs)
        context['form'].fields[
            'category'].queryset = models.Category.objects.all_my_categories(
                self.request.user)
        context['form'].fields[
            'subcategory'].queryset = models.SubCategory.objects.filter(
                category__id=self.get_object().subcategory.category.pk)
        context['form'].fields[
            'category'].initial = self.get_object().subcategory.category.pk

        url = reverse('budget:update_transactions_uploaded',
                      kwargs={'pk': self.kwargs.get('pk')})

        context['url_action'] = url
        return context

    def form_valid(self, form):
        self.object = self.get_object()
        subcategory = models.SubCategory.objects.get(
            pk=self.request.POST['subcategory'])
        self.model.objects.filter(
            description=self.object.description,
            verified=False).update(
            subcategory=subcategory)

        return super(UpdateUploadTransaction, self).form_valid(form)

    def get(self, request, *args, **kwargs):

        response = super(UpdateUploadTransaction, self).get(
            request, *args, **kwargs)
        if self.request.is_ajax():
            return response
        return HttpResponseForbidden()

    def get_success_url(self):
        return reverse('budget:accounts_sync_file',
                       kwargs={'account_pk': self.get_object().account.id})


class ImportTransaction(LoginRequiredMixin, FormView):
    template_name = 'import_transaction_file.html'
    form_class = ImportTransactionForm
    model = models.TransactionUploaded

    def get_context_data(self, **kwargs):
        context = super(ImportTransaction, self).get_context_data(**kwargs)
        account = self.get_account()
        context['account'] = account
        context['form'].fields[
            'template_file'].queryset = models.TemplateFile.objects.filter(
                bank=account.bank)
        context['transactions'] = self.model.objects.pending_transactions(
            self.request.user, account)
        return context

    def form_valid(self, form):
        file = self.request.FILES['file']
        template_file = models.TemplateFile.objects.get(
            pk=self.request.POST['template_file'])
        template_file.import_file(file,
                                  self.get_account(),
                                  self.request.user)
        return super(ImportTransaction, self).form_valid(form)

    def get_initial(self):
        return {'account': self.kwargs.get('account_pk')}

    def get_account(self):
        account = models.Account.objects.get(
            pk=self.kwargs.get('account_pk'))

        if not account.owners.filter(username__in=[
                                     self.request.user]).count():
            raise Http404

        return account

    def get_success_url(self):
        return reverse('budget:accounts_sync_file',
                       kwargs={'account_pk': self.kwargs.get('account_pk')})


class PostTransactionUploaded(LoginRequiredMixin, RedirectView):

    def post(self, request, *args, **kwargs):

        if self.request.POST['submit'] == 'Submit Validation':
            self.register_transaction(request)
        else:
            self.delete_transactions(request)

        self.url = reverse('budget:accounts_sync_file',
                           kwargs={'account_pk': request.POST['account']})
        return super(PostTransactionUploaded, self).get(
            request, args, **kwargs)

    def register_transaction(self, request):

        uploadeds = self.request.POST.getlist('uploaded_transaction')

        for trx in uploadeds:

            trx_up = models.TransactionUploaded.objects.get(
                pk=trx.replace(',', ''))
            transaction = models.Transaction.objects.create(
                account=trx_up.account,
                trx_type=trx_up.trx_type,
                subcategory=trx_up.subcategory,
                currency=trx_up.account.currency,
                place=trx_up.description,
                date=trx_up.date,
                amount=trx_up.amount,
                amount_account=trx_up.amount,
                exchange=1,
                user_insert=trx_up.user_insert
            )

            self.add_history_data(transaction)

            trx_up.verified = True
            trx_up.trx_match = transaction
            trx_up.save()

    def add_history_data(self, transaction):

        models.SubcategoryByDescription.objects.create(
            subcategory=transaction.subcategory,
            description=transaction.place,
            user_insert=transaction.user_insert
        )

    def delete_transactions(self, request):

        uploadeds = self.request.POST.getlist('uploaded_transaction')

        models.TransactionUploaded.objects.filter(
            pk__in=uploadeds).delete()

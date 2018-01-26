  var formAjaxSubmit = function(form, modal) {
      $(form).submit(function (e) {
          e.preventDefault();
          $.ajax({
              type: $(this).attr('method'),
              url: $(this).attr('action'),
              data: $(this).serialize(),
              success: function (xhr, ajaxOptions, thrownError) {
                  if ( $(xhr).find('.has-error').length > 0 ) {
                     $(modal).find('.modal-body').html(xhr);
                     formAjaxSubmit(form, modal);
                 } else {
                     $(modal).modal('toggle');
                 }
             },
             error: function (xhr, ajaxOptions, thrownError) {
                 // handle response errors here
             }
         });
     });
 }
 $('#comment-button').click(function() {
     $('#form-modal-body').load('/test-form/', function () {
         $('#form-modal').modal('toggle');
         formAjaxSubmit('#form-modal-body form', '#form-modal');
     });
 }
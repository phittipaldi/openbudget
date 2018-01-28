var date_format = 'dd/mm/yyyy'
    
var formAjaxSubmit = function(form, tab, after_success=null) {
    $(form).submit(function (e) {
        e.preventDefault();
        var url = $(this).attr('action')
        var data = new FormData($(form)[0]);
        $.ajax({
            type: $(this).attr('method'),
            url: url,
            data: data,
            processData: false,
            contentType: false,
            cache : false,
            success: function (xhr, ajaxOptions, thrownError) {
                if ( $(xhr).find('.has-error').length > 0 ) {
                    $(tab).html(xhr)
                    formAjaxSubmit(form, tab, after_success);
                    refresh_selectpicker()
                } else {
                    if (after_success){
                        after_success(xhr)
                    } else {
                        window.location.reload()
                    }
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                // handle response errors here
            }
        });
    });
} // formAjaxSubmit

var getAjaxUrl = function(url, post_success=null) {
    $.ajax({
        url: url,
        success: function(values){
            if (post_success){
                post_success(values)
            }
        }
    })
}

var postAjaxUrl = function(url, post_success=null) {
    var token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        type: 'POST',
        url: url,
        data: { 'csrfmiddlewaretoken': token },
        success: function(values){
            if (post_success){
                post_success(values)
            }
        }
    })
}

var attachClickLoadModal = function(selector, modal, after_success=null, data_url=false){
    /*
        Uso:
        var selector = '.anular'
        var modal = '#modal'
        si pasamos una function como tercer parametro
        la ejecutara luego de postear y recibir success.
        si se pasa como cuarto parametro, data_url=True
        tratara de buscar la url de ptopiedad data-url del elemento.
        attachClickLoadModal(selector, modal, after_success)
     
     */

    var modal_body = modal + ' .modal-body'
    var modal_form = modal_body + ' form'
    
    $(selector).on('click', function(e) {
        e.preventDefault()
        if (data_url){
            var url = $(this).data('url')
        } else {
            var url = $(this).attr('href')
        }
        
        $(modal_body).load(url, function () {
            $(modal).modal('toggle');
            formAjaxSubmit(modal_form, modal_body, after_success);
        });
    })
}//end attachClickLoadModal

var select_buscable = function() {
    $('.slt-search').selectpicker({
        liveSearch:true, 
    });
}
var refresh_select_buscable = function() {
    $('.slt-search').selectpicker('refresh');
}

var refresh_selectpicker = function() {
    $('.selectpicker').selectpicker('refresh');
}

var date_picker = function() {
    $( ".dateinput" ).datepicker({
          autoclose: true,
          format: date_format,
    })
}

var notificar = function(texto){
    $.niftyNoty({
        type: 'dark',
        container : 'floating',
        html : texto,
        timer : 5000
    });
}
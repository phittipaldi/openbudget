$(function() {

    currency_filter =  function() {
    
        $("#id_currency").on('change', function(e){ 
            var id = $("#id_currency").val();
            if (id == '')
                id = 0;

            var url = '/utils/currency_rate/json/'+ id +'/'
            $.ajax({
                url: url,
                success: function(data){
                    $("#id_ratio").val(data.ratio)
                    $("#id_inverse_ratio").val(data.inverse_ratio)
                    var label = $("label[for=id_ratio]").text()
                    $("label[for=id_ratio]").text(label + " ( " + data.ratio_desc + " )");
                    label = $("label[for=id_inverse_ratio]").text()
                    $("label[for=id_inverse_ratio]").text(label + " ( " + data.inverse_ratio_desc + " )");
                }
            })
            
        })
    }//end category_filter

    currency_filter()
});

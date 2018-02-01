$(function() {

    periods_filter =  function() {
    
        $("#id_budget").on('change', function(e){ 
            var id = $("#id_budget").val();
            if (id == '')
                id = 0;

            var url = '/budget/periods/json/'+ id +'/'
            $.ajax({
                url: url,
                success: function(data){
                    var options = $('[name="period"]')
                    options.empty()
                    options.append($("<option />").val("").text("-------------"));
                    $.each(data, function(idx, val) {
                        options.append($("<option />").val(val.id).text(val.name));
                    });
                    //refresh_select_buscable()
                }
            })
            
        })
    }//end category_filter

    periods_filter()
});

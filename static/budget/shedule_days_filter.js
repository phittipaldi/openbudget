$(function() {

    days_filter =  function() {
    
        $("#id_period_type").on('change', function(e){ 
            var id = $("#id_period_type").val();
            if (id == '')
                id = 0;

            var url = '/budget/recurrent/days/'+ id +'/json/'
            $.ajax({
                url: url,
                success: function(data){
                    var options = $('[name="day"]')
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

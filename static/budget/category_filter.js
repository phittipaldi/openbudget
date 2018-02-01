$(function() {

    account_filter =  function() {
    
        $("#id_account").on('change', function(e){ 
            var id = $("#id_account").val();
            if (id == '')
                id = 0;

            var url = '/budget/account/category/json/'+ id +'/'
            $.ajax({
                url: url,
                success: function(data){
                    var options = $('[name="category"]')
                    options.empty()
                    options.append($("<option />").val("").text("---------"));
                    $.each(data, function(idx, val) {
                        options.append($("<option />").val(val.id).text(val.name));
                    });
                    //refresh_select_buscable()
                }
            })
            
        })
    }//end category_filter

    category_filter =  function() {
    
        $("#id_category").on('change', function(e){ 
            var id = $("#id_category").val();
            if (id == '')
                id = 0;

            var url = '/budget/category/subcategory/json/'+ id +'/'
            $.ajax({
                url: url,
                success: function(data){
                    var options = $('[name="subcategory"]')
                    options.empty()
                    options.append($("<option />").val("").text("---------"));
                    $.each(data, function(idx, val) {
                        options.append($("<option />").val(val.id).text(val.name));
                    });
                    //refresh_select_buscable()
                }
            })
            
        })
    }//end category_filter

    account_filter()
    category_filter()
});

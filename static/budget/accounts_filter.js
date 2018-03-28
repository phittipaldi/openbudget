

$(function() {


    accounts_filter =  function() {
        
        $("#id_currency").on('change', function(e){ 

            var id = $("#id_currency").val();
            if (id == '')
                id = 0;

            var url = '/budget/accounts/'+ id +'/json/'

            $.ajax({
                url: url,
                success: function(data){
                    $('#id_accounts').empty();
                    $.each(data, function(idx, val) {
                        append_checkbox(val);
                    });
                    //refresh_select_buscable()
                }
            })
            
        })
    }//end category_filter


    function append_checkbox(account, index)
    {
        var ul = document.getElementById('id_accounts');
        var li = document.createElement('li');

        var checkbox = document.createElement('input');
        checkbox.type = "checkbox";
        checkbox.name = "accounts";
        checkbox.value = account.id;
        checkbox.id = "id_accounts_" + index;

        var label = document.createElement('label')
        label.htmlFor = "id_accounts_" + index;
        label.appendChild(document.createTextNode(' ' + account.name));

        li.appendChild(checkbox);
        li.appendChild(label)
        //li.appendChild(document.createTextNode(' ' + account.name));
        ul.appendChild(li); 

    }

    accounts_filter()

});



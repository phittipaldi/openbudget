$(function(){


    check_all = function(value){

        var aa = document.querySelectorAll("input[type=checkbox]");
        for (var i = 0; i < aa.length; i++){
            aa[i].checked = value;
        }
    }

    $('#check_all').click(function() {
        if (this.checked)
            check_all(true);
        else
            check_all(false);
    });


});
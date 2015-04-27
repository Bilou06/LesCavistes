/**
 * Created by Sylvain on 14/04/2015.
 */

String.prototype.splice = function( idx, rem, s ) {
    return (this.slice(0,idx) + s + this.slice(idx + Math.abs(rem)));
};

function countChecked(){
    var count = 0;
   $(".action-select").each(function () {
                if ($(this).is(":checked")) {
                    count +=1;
                }
            });
    return count;
}

function getChecked(){
    var index = [];
    $(".action-select").each(function () {
                if ($(this).is(":checked")) {
                    index.push($(this).attr("value"));
                }
            });
    return index;
}

function removeChecked(){
    window.location.href = "/wineshops/confirm_remove/"+getChecked().join(',');
}

function stockChecked(status){
    var url = (status ? "/wineshops/in_wines/" : "/wineshops/out_wines/");
     $.get(
        url+getChecked().join(','),
         {},
        function(){
            location.reload();
        }
    );

}


function sort(order){
    var column = ['','column-producer', 'column-country','column-region', 'column-area', 'column-color', 'column-varietal', 'column-classification', 'column-vintage', 'column-capacity', 'column-price_min', 'column-price_max', 'column-in_stock'][Math.abs(order)];
    $(".sortable").removeClass("sorted");
    if (order>0) {
        $("a[href^='?o=" + order + "']").each(function () {
            this.href = this.href.replace("/?o=", "/?o=-")
        });
        $("."+column).addClass("sorted ascending");
    }else{
        $("."+column).addClass("sorted descending");
    }
}

$(document).ready(function () {

    $('#count-total').text($(".action-select").length)

    $("#action-toggle").change(function () {
        if ($(this).is(":checked")) {
            $(".action-select").each(function () {
                $(this).prop('checked', true);
            })
        } else {
            $(".action-select").each(function () {
                $(this).prop('checked', false);
            })
        }
        $('#count-selected').text(countChecked())
    });

    $('.action-select').change(function(){
        $('#count-selected').text(countChecked())
    });

    $('.form-button').click(function()
    {
        var count = countChecked();
        if(count ==0 ){
            alert("Aucun vin sélectionné");
            return;
        }

        //var action = $("#action option:selected").prop('value');
        var action = $("#action").val();
        if(action.length == 0){
            alert('Aucune action sélectionnée, veuillez sélectionner une action');
            return
        }

        if(action == "delete_selected"){
            removeChecked();
        } else if (action == "in_stock_selected"){
            stockChecked(true);
        } else if (action == "out_stock_selected") {
            stockChecked(false);
        }
    });

});


/**
 * Created by Sylvain on 14/04/2015.
 */

function countChecked(){
    var count = 0;
   $(".action-select").each(function () {
                if ($(this).is(":checked")) {
                    count +=1;
                };
            })
    return count;
}

function removeChecked(){
    var index = [];
    $(".action-select").each(function () {
                if ($(this).is(":checked")) {
                    index.push($(this).attr("value"));
                };
            })
    window.location.href = "/wineshops/confirm_remove/"+index.join(',')
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
    })

    $('.form-button').click(function()
    {
        count = countChecked();
        if(count ==0 ){
            alert("Aucun vin sélectionné");
            return;
        }

        action = $("#action").val();
        if(action.length == 0){
            alert('Aucune action sélectionnée, veuillez sélectionner une action');
            return
        }

        if(action == "delete_selected"){
            removeChecked();
        }
    });

});


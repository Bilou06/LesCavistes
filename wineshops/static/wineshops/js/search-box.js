/**
 * Created by Sylvain on 17/04/2015.
 */


$(document).ready(function () {

    var text1 = $("#tfq1b").val();
    if (text1 == ""){
        text1 = "Quel vin ? Vide pour tous";
        $("#tfq1b").val(text1);
    }

    var text2 = $("#tfq2b").val();
    if (text2 == ""){
        text2 = "Où ? Entrez une ville, une adresse"; //duplicated in the view
        $("#tfq2b").val(text2);
    }

    $(function () {
        $("#tfq1b").click(function () {
            if ($("#tfq1b").val() == text1) {
                $("#tfq1b").val("");
            }
        });
    });

    $(function () {
        $("#tfq2b").click(function () {
            if ($("#tfq2b").val() == text2) {
                $("#tfq2b").val("");
            }
        });
    });
});
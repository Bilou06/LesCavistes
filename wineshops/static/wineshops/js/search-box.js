/**
 * Created by Sylvain on 17/04/2015.
 */

var text1, text2;
var finished = false;

function mainSearch() {
    if (finished) {
        return true;
    }
    codeAddress();
    return false;
}

function error() {
    $("#dialog-message").show();
}

function codeAddress() {
    var address = $("#tfq2b").val();
    if (address == ref2) {
        error();
        return false;
    } else {
        geocoder = new google.maps.Geocoder();
        geocoder.geocode({'address': address}, function (results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    $("#id_latitude").attr("value", results[0].geometry.location.lat());
                    $("#id_longitude").attr("value", results[0].geometry.location.lng());
                    if (field1.val() == ref1) {
                        field1.val("");
                    }
                    finished = true;
                    $("#tfnewsearch").submit();
                    $("#tftopsearch").submit();
                }
                else {
                    error();
                    return false;
                }
            }
        )
        ;
    }
    return true;
}

var ref1 = "Tous les vins";
var ref2 = "Où ? Entrez une ville, une adresse"//duplicated in the view
var field1, field2;

$(document).ready(function () {

    field1 = $("#tfq1b")
    text1 = field1.val();
    if (text1 == "") {
        text1 = ref1;
        field1.val(text1);
    }

    field2 = $("#tfq2b")
    text2 = field2.val();
    if (text2 == "") {
        text2 = ref2;
        field2.val(text2);
        getLocation();
    }

    field1.click(function () {
        if (field1.val() == ref1) {
            field1.val("");
            field1.addClass("tftextinput_modified")
        }
    });

    field2.click(function () {
        if (field2.val() == ref2) {
            field2.val("");
            field1.addClass("tftextinput_modified")
        }
    });

});


function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    }
}
function showPosition(position) {
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

    geocoder.geocode({'latLng': latlng}, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                field2.val(results[0].formatted_address)
                field2.addClass("tftextinput_modified")
            }
        }
    )
    ;
}


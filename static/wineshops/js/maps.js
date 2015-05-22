/**
 * Created by Sylvain on 17/04/2015.
 */
var geocoder;
var map;

var addressFields = ["id_address", "id_city", "id_zip_code", "id_country"];


function readAddress() {
    var values = jQuery.map(addressFields, function (field) {
        return document.getElementById(field).value
    });
    return values.join(', ');
}
var previousAddress = "";


function initialize() {
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(48.856614, 2.3522);
    var mapOptions = {
        zoom: 8,
        center: latlng
    };
    $("#map-canvas").css({opacity: 0, zoom: 0});
    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

}

function codeAddress() {
    var address = readAddress();
    if (address == previousAddress) {
        return;
    }
    previousAddress = address;
    if (address.lastIndexOf(['', '', ''].join(', '), 0) === 0) {
        return;
    } //nothing interesting yet
    geocoder.geocode({'address': address}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setZoom(15);
            map.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
                map: map,
                position: results[0].geometry.location
            });
            $("#map-canvas").css({opacity: 1, zoom: 1});
            $('#id_latitude').attr("value", results[0].geometry.location.lat());
            $('#id_longitude').attr("value", results[0].geometry.location.lng());
        } else {
            alert("Impossible de géolocaliser cette adresse: " + address + status);
        }
    });
}


$(document).ready(function () {

    previousAddress = "";

    jQuery.each(addressFields, function (field) {
        $('#' + addressFields[field]).attr("onblur", "codeAddress();");
    });

    initialize();
    google.maps.event.addDomListener(window, 'load', codeAddress);
});


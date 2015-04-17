/**
 * Created by Sylvain on 17/04/2015.
 */
var geocoder;
var map;

var addressFields = ["id_address", "id_city", "id_zip_code", "id_country" ];


function readAddress(){
        var values = addressFields.map(function(field){
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
    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
}

function codeAddress() {
    var address = readAddress();
    if (address == previousAddress){return;}
    previousAddress = address;
    if (address.lastIndexOf(['','',''].join(', '), 0) === 0){return;} //nothing interesting yet
    geocoder.geocode({'address': address}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setZoom(15);
            map.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
                map: map,
                position: results[0].geometry.location
            });
            $('#id_latitude').attr("value",  results[0].geometry.location.lat());
            $('#id_longitude').attr("value",  results[0].geometry.location.lng());
        } else {
            alert("Impossible de géolocaliser cette adresse: " + address + status);
        }
    });
}


$(document).ready(function () {

    previousAddress = ""

    addressFields.forEach(function(field){
       $('#'+field).attr("onblur", "codeAddress();");
    });

    initialize();
    google.maps.event.addDomListener(window, 'load', codeAddress);
});


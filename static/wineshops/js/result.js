/**
 * Created by Sylvain on 20/04/2015.
 */

var map;

function initialize() {
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng($("#id_latitude").val(), $("#id_longitude").val());
    var mapOptions = {
        zoom: 14,
        center: latlng,
        content: "cavistes proches de chez vous"
    };
    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
    var marker = new google.maps.Marker({
        position: latlng,
        map: map,
        clickable: false

    });
}

function addMarkers() {
    var bounds = new google.maps.LatLngBounds();
    bounds.extend(new google.maps.LatLng($("#id_latitude").val(), $("#id_longitude").val()));
    var i = 0;
    $(".shop-lat-lng").each(function () {
        i++;
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng($(this).data('lat'), $(this).data('lng')),
            title: $(this).data('title'),
            map: map,
            animation: google.maps.Animation.DROP,
            icon: '/static/wineshops/images/mapicons/number_' + i.toString() + '.png'
        });

        var contentString = $(this).siblings('.td-infoshop').find(".bloc-info-shop").html();

        var infowindow = new google.maps.InfoWindow({
            content: contentString,
            maxWidth: 400
        });
        google.maps.event.addListener(marker, 'click', function () {
            infowindow.open(map, marker);
        });

        bounds.extend(marker.getPosition());

    });
    map.fitBounds(bounds);
}

$(document).ready(function () {

    $(".infoshop").click(function (event) {
        $(this).find(".bloc-info-shop").show();
        event.stopPropagation();
    });

    $('html').click(function () {
        $(".bloc-info-shop").hide();
    });

    initialize();
    addMarkers();
});
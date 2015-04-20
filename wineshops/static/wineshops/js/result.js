/**
 * Created by Sylvain on 20/04/2015.
 */


$(document).ready(function () {

    $(".infoshop").click(function(){
        $(this).find(".bloc-info-shop").show();
        event.stopPropagation();
    });

    $('html').click(function() {
        $(".bloc-info-shop").hide();
    });
});
/**
 * Created by Sylvain on 21/04/2015.
 */


(function ($) {
    $.widget("custom.combobox", {
        _create: function () {
            this.wrapper = $("<span>")
                .addClass("custom-combobox")
                .insertAfter(this.element);

            this.element.hide();
            this._createAutocomplete();
            this._createShowAllButton();

        },

        _createAutocomplete: function () {
            var selected = this.element.children(":selected"),
                value = selected.val() ? selected.text() : "";

            this.input = $("<input>")
                .appendTo(this.wrapper)
                .val(value)
                .attr("title", "")
                .addClass("custom-combobox-input ui-widget ui-widget-content ui-state-default ui-corner-left")
                .autocomplete({
                    delay: 0,
                    minLength: 0,
                    source: $.proxy(this, "_source")
                })
                .tooltip({
                    tooltipClass: "ui-state-highlight"
                });


            var input = this.input;
            if ($(this.element).attr('id') == "id_country") {
                this.element.children("option").each(function () {
                    if (this.value == $('#former_country').val()) {
                        this.selected = valid = true;
                        input.val(this.text);
                    }
                })
            }
            this._updateOptions();

            this._on(this.input, {
                autocompleteselect: function (event, ui) {
                    ui.item.option.selected = true;
                    this._trigger("select", event, {
                        item: ui.item.option
                    });
                },

                autocompletechange: "_removeIfInvalid"
            });
        },

        _createShowAllButton: function () {
            var input = this.input,
                wasOpen = false;

            $("<a>")
                .appendTo(this.wrapper)
                .button({
                    icons: {
                        primary: "ui-icon-triangle-1-s"
                    },
                    text: false
                })
                .removeClass("ui-corner-all")
                .addClass("custom-combobox-toggle ui-corner-right")
                .mousedown(function () {
                    wasOpen = input.autocomplete("widget").is(":visible");
                })
                .click(function () {
                    input.focus();

                    // Close if already visible
                    if (wasOpen) {
                        return;
                    }

                    // Pass empty string as value to search for, displaying all results
                    input.autocomplete("search", "");
                });
        },

        _source: function (request, response) {
            var matcher = new RegExp($.ui.autocomplete.escapeRegex(request.term), "i");
            response(this.element.children("option").map(function () {
                var text = $(this).text();
                if (this.value && ( !request.term || matcher.test(text) ))
                    return {
                        label: text,
                        value: text,
                        option: this
                    };
            }));
        },

        _removeIfInvalid: function (event, ui) {

            // Change value in hidden form
            this._updateHidden();
            this._updateOptions();
        },

        _updateHidden: function(){
            $("#" + $(this.element).attr('id') + "_hidden").val(this.input.val());
        },

        _updateOptions: function () {
            // Search for a match (case-insensitive)
            var value = this.input.val(),
                valueLowerCase = value.toLowerCase(),
                valid = false;

            var index = 0;
            this.element.children("option").each(function () {
                if ($(this).text().toLowerCase() === valueLowerCase) {
                    this.selected = valid = true;
                    index = this.value;
                }
            });

            // update options
            if ($(this.element).attr('id') == "id_country") {
                var id_region = $('#id_region');
                id_region
                    .find('option')
                    .remove()
                    .end()
                    .append('<option value="" selected="selected">---------</option>');
                $.get('/wineshops/regions',
                    {'country_id': index},
                    function (data) {
                        var regions = data.split('|');
                        for (index in regions) {
                            var region = regions[index].split('#');
                            id_region.append(new Option(region[0], region[1]));
                        }

                        id_region.children("option").each(function () {
                            if (this.value == $('#former_region').val()) {
                                this.selected = valid = true;
                                id_region.next().find('input').val(this.text);
                            }

                        });

                    })
            } else if ($(this.element).attr('id') == "id_region") {
                var id_area = $('#id_area');
                id_area
                    .find('option')
                    .remove()
                    .end()
                    .append('<option value="" selected="selected">---------</option>');
                $.get('/wineshops/areas',
                    {'region_id': index},
                    function (data) {
                        regions = data.split('|');
                        for (index in regions) {
                            region = regions[index].split('#');
                            id_area.append(new Option(region[0], region[1]));
                        }

                        id_area.children("option").each(function () {
                            if (this.value == $('#former_area').val()) {
                                this.selected = valid = true;
                                id_area.next().find('input').val(this.text);
                            }

                        });
                    });
            }
        },

        _destroy: function () {
            this.wrapper.remove();
            this.element.show();
        }
    });
})(jQuery);

$(function () {
    $("#id_country").combobox();
    $("#id_region").combobox();
    $("#id_area").combobox();
});


function setHiddenFields(){
    $("#id_country_hidden").val($("#id_country").next().find('input').val());
    $("#id_region_hidden").val($("#id_region").next().find('input').val());
    $("#id_area_hidden").val($("#id_area").next().find('input').val());
};
this.ckan.module('dataset-visibility-select', function ($, _) {
    return {
        initialize: function() {
            var sandbox = this.sandbox;
            this._onChange = jQuery.proxy(this._onChange, this);
            this.el.on('change', this._onChange);
            this._onChange();
        },
        _onChange: function() {
            let visibility = $("#field-private").find(":selected").text()
            this.sandbox.publish("change:visibility", visibility)
        }
    }
})

this.ckan.module('public-visible-warning', function ($, _) {
    return {
        initialize: function() {
            this.sandbox.subscribe("change:visibility", function(visibility){
                if(visibility !== "Public") {
                    $("#public-visible-warning").hide("slow");
                } else {
                    $("#public-visible-warning").show("slow");
                }
            });
        }
    }
})
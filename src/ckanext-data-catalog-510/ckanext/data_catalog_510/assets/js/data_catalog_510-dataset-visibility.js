this.ckan.module('dataset-visibility-select', function ($, _) {
    return {
        initialize: function() {
            this._onChange = jQuery.proxy(this._onChange, this);
            this.el.on('change', this._onChange);
            this._onChange();
        },
        _onChange: function() {
            let params = {};
            if ($("#field-private").find(":selected").text() === "Public") {
                params['show'] = true;
            } else {
                params['show'] = false;
            }
            params['id'] = $('#public-visible-warning').attr('id');
            this.sandbox.publish("change:showWarning", params);
        }
    }
});
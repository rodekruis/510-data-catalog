/*
* dataset-visibility-select
* This JavaScript module is used in the Visibility field of Dataset Form page 
* to display a warning if the dataset's visibility is set to Public.
* It internally triggers the warning-display common module.
*/
this.ckan.module('dataset-visibility-select', function ($, _) {
    return {
        initialize: function() {
            this._onChange = jQuery.proxy(this._onChange, this);
            this.el.on('change', this._onChange);
            this._onChange();
        },
        _onChange: function() {
            let params_public = {};
            if ($("#field-private").find(":selected").text() === "Public") {
                params_public['show'] = true;
            } else {
                params_public['show'] = false;
            }
            params_public['id'] = $('#public-visible-warning').attr('id');
            this.sandbox.publish("change:showWarning", params_public);
        }
    }
});
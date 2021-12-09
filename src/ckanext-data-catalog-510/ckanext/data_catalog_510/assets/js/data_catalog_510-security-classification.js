this.ckan.module('security-classification-select', function ($, _) {
    return {
        initialize: function() {
            this._onChange = jQuery.proxy(this._onChange, this);
            this.el.on('change', this._onChange);
            this._onChange();
        },
        _onChange: function() {
            lowSecWarnId = $('#low-security-warning').attr('id');
            normalSecWarnId = $('#normal-security-warning').attr('id');
            if ($("#field-security_classification").find(":selected").text() === "Normal") {
                this.displayWarning(lowSecWarnId, false);
                this.displayWarning(normalSecWarnId, true);
            } else if ($("#field-security_classification").find(":selected").text() === "Low"){
                this.displayWarning(normalSecWarnId, false);
                this.displayWarning(lowSecWarnId, true);
            } else {
                this.displayWarning(normalSecWarnId, false);
                this.displayWarning(lowSecWarnId, false);
            }
        },

        displayWarning: function(id, showBool) {
            let params = {
                id: id,
                show: showBool
            }
            this.sandbox.publish("change:showWarning", params)
        }
    }
});
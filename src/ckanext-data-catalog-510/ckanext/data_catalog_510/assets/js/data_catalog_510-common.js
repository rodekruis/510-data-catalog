this.ckan.module('warning-display', function ($, _) {
    return {
        initialize: function() {
            this.sandbox.subscribe("change:showWarning", function(params){
                if(params['show']) {
                    $('#' + params['id']).show("slow");
                } else {
                    $('#' + params['id']).hide("slow");
                }
            });
        }
    }
});
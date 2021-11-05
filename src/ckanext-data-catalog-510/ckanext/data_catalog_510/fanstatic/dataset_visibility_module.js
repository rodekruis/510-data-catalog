/*
this.ckan.module('dataset-visibility', function ($, _) {
    return {
        initialize: function() {
            let visibility = ""
            $('#field-private').change(function() {
                visibility = $(this).find(":selected").text
            })
            this.sandbox.publish("visibility:public", visibility)
        }
    }
})

this.ckan.module('public-visible-warning', function ($, _) {
    return {
        initialize: function() {
            $('#field-private').change(function() {
                visibility = $(this).find(":selected").text
            })
            this.sandbox.subscribe("visibility:public", function(visibility){
                if(visibility !== "Public") {
                    $("#public-visible-warning").hide("slow");
                } 
            })
        }
    }
})
*/
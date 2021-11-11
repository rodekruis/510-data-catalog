/*
* Common.js
* This file contians modules that is not tied to a specific HTML element.
* Ensure that module requirements are followed during implementation.
*/

/* warning-display
* This JavaScript module shows/hides the HTML element that the module is applied to.
* All modules that this module needs to be applied to must have this module's name in their 'data-module' tag attribute.
* 
* This module requires parameters to be passed through the sandbox's publish() as a JavaScript Object.
* The parameter object should contain two keys:
* id - the id attribute value of the HTML tag this module is applied to.
* show - boolean value depicting action to be performed by the module 
* (params['show'] = true - shows the element)
* (params['show'] = flase - hides the element)
*
* Other modules calling this module must publish to 'change:showWarning' topic.
*/
this.ckan.module('warning-display', function ($, _) {
    return {
        initialize: function () {
            this.sandbox.subscribe("change:showWarning", function (params) {
                try {
                    if (params['show']) {
                        $('#' + params['id']).show("slow");
                    } else {
                        $('#' + params['id']).hide("slow");
                    }
                } catch (err) {
                    console.error(err);
                }
            });
        }
    }
});
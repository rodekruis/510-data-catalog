this.ckan.module('request-data-btn', function ($, _) {
    return {
        initialize: function() {
            this._onClick = jQuery.proxy(this._onClick, this);
            this.el.on('click', this._onClick);
        },
        _onClick: function() {
            let mailToUrl = $("#request-data-btn").data('mailto');
            let mailArray = mailToUrl.split("&subject");
            mailArray[0] = mailArray[0].replace(/@@/g, ".");
            mailToUrl = mailArray.join('&subject');
            setTimeout(function(){document.location.href = mailToUrl},0);
        }
    }
});
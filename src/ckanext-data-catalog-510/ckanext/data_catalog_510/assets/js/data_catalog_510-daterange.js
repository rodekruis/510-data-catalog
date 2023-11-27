
this.ckan.module('daterange', function ($) {
  return {
    initialize: function () {
        

        const searchParams = new URLSearchParams(window.location.search);
        const query = searchParams.get('q')
        if(query) {
        const hasDateAdded = query.search('date_added')

        if(hasDateAdded >= 0) {
            const closingPosition = query.indexOf(']', hasDateAdded + 11)
            const dateRange = query.substring(hasDateAdded + 12, closingPosition).replaceAll('"', '').split(' TO ')
            
            $('#startrange').val(dateRange[0]);
            $('#endrange').val(dateRange[1]);

            let message = document.querySelector("#search_title").innerHTML

            message = message.split('"date_added')[0]

            message = `${message} "${dateRange[0]}" To "${dateRange[1]}"`

            document.querySelector("#search_title").innerHTML = message
        }
     } else {
            $('#startrange').val('');
            $('#endrange').val('');
        }

        
      this._onClick = jQuery.proxy(this._onClick, this);
      this.el.on("click", this._onClick);
    },
    _onClick: async function() {
        const start = $("#startrange").val()
        const end = $("#endrange").val()
        var link = document.createElement("a");  // Create with DOM
        link.href = `/dataset?q=date_added:[%22${start}%22%20TO%20%22${end}%22]`;
        link.click()
    }
  };
});
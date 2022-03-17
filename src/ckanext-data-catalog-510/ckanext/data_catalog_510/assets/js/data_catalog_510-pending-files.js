this.ckan.module("ignore-pending-files", function ($, _) {
  return {
    initialize: function () {
      this._onClick = jQuery.proxy(this._onClick, this);
      this.el.on("click", this._onClick);
      this.showConfirmMessage(false);
      this.showErrorMessage(false);
    },
    _onClick: async function () {
      try {
        let params = {};
        let ignore_data = $("textarea#field-ignore_data").val();
        let siteUrl = $("#ignore_files_save_button").data("siteurl");
        params["url"] =
          siteUrl + "/api/3/action/update_ignore_pending_file_list";
        params["data"] = ignore_data;
        response = await $.ajax({
          type: "POST",
          url: params["url"],
          data: { ignore_data: params["data"] },
        });
        if (response["result"]) {
          this.showConfirmMessage(true);
          setTimeout(function () {
            $("#file-saved-notif").hide("slow");
          }, 5000);
        } else {
          this.showErrorMessage(true);
          setTimeout(function () {
            $("#file-not-saved-notif").hide("slow");
          }, 5000);
        }
      } catch (err) {
        console.log(err);
      }
    },
    showConfirmMessage: function (show) {
      let notif_params = {
        id: $("#file-saved-notif").attr("id"),
        show: show,
      };
      this.sandbox.publish("change:showWarning", notif_params);
    },
    showErrorMessage: function (show) {
      let notif_params = {
        id: $("#file-not-saved-notif").attr("id"),
        show: show,
      };
      this.sandbox.publish("change:showWarning", notif_params);
    },
  };
});

this.ckan.module("get_pending_files_list", function ($, _) {
  return {
    initialize: function () {
      this._onClick = jQuery.proxy(this._onClick, this);
      this.el.on("click", this._onClick);
      this.showInfoMessage(false);
      this.showSuccessMessage(false);
      this.showFailedMessage(false);
    },
    _onClick: async function () {
      try {
        let params = {};
        let siteUrl = $("#generate_pending_files_list_button").data("siteurl");
        params["url"] = siteUrl + "/api/3/action/generate_pending_files_list";
        this.showInfoMessage(true);
        response = await $.ajax({
          type: "POST",
          url: params["url"],
          data: {},
        });
        if (response) {
          this.showInfoMessage(false);
          if (response["result"]) {
            this.showSuccessMessage(true);
            setTimeout(function () {
              $("#pending-file-created-notif").hide("slow");
            }, 5000);
          } else {
            this.showFailedMessage(true);
            setTimeout(function () {
              $("#pending-file-not-created-notif").hide("slow");
            }, 5000);
          }
        }
      } catch (err) {
        console.log(err);
      }
    },
    showInfoMessage: function (show) {
      let notif_params = {
        id: $("#pending-file-wait-notif").attr("id"),
        show: show,
      };
      this.sandbox.publish("change:showWarning", notif_params);
    },
    showSuccessMessage: function (show) {
      let notif_params = {
        id: $("#pending-file-created-notif").attr("id"),
        show: show,
      };
      this.sandbox.publish("change:showWarning", notif_params);
    },
    showFailedMessage: function (show) {
      let notif_params = {
        id: $("#pending-file-not-created-notif").attr("id"),
        show: show,
      };
      this.sandbox.publish("change:showWarning", notif_params);
    },
  };
});

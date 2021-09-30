/* Image Upload
 *
 */
this.ckan.module("fetch-sql", function ($) {
  return {
    /* options object can be extended using data-module-* attributes */

    /* Initialises the module setting up elements and event listeners.
     *
     * Returns nothing.
     */
    initialize: async function () {
      $.proxyAll(this, /_on/);
      if (this.options.connection_type_selected) {
        let response = await this.executeAPI("get_all_dbs", {});
        await this.handleAPIResponse(response, "database_connection_type");
        this.setValues(
          "database_connection_type",
          this.options.connection_type_selected
        );
      }
      if (this.options.connection_selected) {
        let response = await this.executeAPI("get_all_dbs", {});
        await this.handleAPIResponse(response, "database_connection_type");
        this.setValues(
          "database_connection_type",
          this.options.connection_selected
        );
      }
    },

    setValues: function (id, option) {
      $(`#${id}`).select2("val", option);
    },

    executeAPI: async function (api, data) {
      let result;
      let url = ckan.url(`/api/3/action/${api}`);
      let headers = {
        "X-CKAN-API-Key": this.options.apiKey,
      };
      try {
        result = await $.ajax({
          type: "POST",
          url: url,
          dataType: "json", //expect html to be returned
          data: data,
          headers: headers,
        });

        return result;
      } catch (error) {
        console.error(error);
      }
    },
    executeRes: async function (id, e) {
      let that = this;
      if (id == "database_connection_type") {
        let database_connection_type = e.val;
        let response = await that.executeAPI("get_db_connections", {
          db_type: database_connection_type,
        });
        await that.handleAPIResponse(response, "database_connection");
        document.getElementById("form_database_connection").style.display =
          "block";
      }
      if (id == "database_connection") {
        let database_connection_type = $(`#database_connection_type`).select2(
          "data"
        ).id;
        let database_connection = e.val;
        let response = await that.executeAPI("get_schemas", {
          db_type: database_connection_type,
          db_name: database_connection,
        });
        await that.handleAPIResponse(response, "schema_name");
        document.getElementById("form_schema_name").style.display = "block";
      }
      if (id == "schema_name") {
        let database_connection_type = $(`#database_connection_type`).select2(
          "data"
        ).id;
        let database_connection = $(`#database_connection`).select2("data").id;
        let schema_name = e.val;
        let response = await that.executeAPI("get_tables", {
          db_type: database_connection_type,
          db_name: database_connection,
          schema: schema_name,
        });
        await that.handleAPIResponse(response, "table_name");
        document.getElementById("form_table_name").style.display = "block";
      }
    },
    handleAPIResponse: function (response, id) {
      let that = this;
      let results = response?.result;
      if (results) {
        if (results.some((result) => result.name)) {
          results = results.map(({ name: id, title: text, ...rest }) => ({
            id,
            text,
            ...rest,
          }));
        } else {
          results = results.map((result) => ({
            id: result,
            text: result,
          }));
        }

        $(`#${id}`)
          .select2({
            data: results,
          })
          .trigger("change");
        $(`#${id}`).on("select2-selecting", async function (e) {
          that.executeRes(id, e);
        });
      }
    },
  };
});

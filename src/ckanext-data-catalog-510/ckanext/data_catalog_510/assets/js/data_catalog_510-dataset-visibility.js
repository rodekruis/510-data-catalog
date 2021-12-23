/*
* dataset-visibility-select
* This JavaScript module is used in the Visibility field of Dataset Form page 
* to display a warning if the dataset's visibility is set to Public.
* It internally triggers the warning-display common module.
* Note: This module has become obsolete since field-private has been removed in favour of field-security_classification.
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

/* 
Snippet code for field-private (from organization.html):

<div class="control-group form-group control-medium">
      <label for="field-private" class="control-label">{{ _('Visibility') }}</label>
      <div class="controls">
        <select id="field-private" name="private" class="form-control" data-module="dataset-visibility-select">
          {% for option in [('True', _('Private')), ('False', _('Public'))] %}
          <option value="{{ option[0] }}" {% if option[0] == data.private|trim %}selected="selected"{% endif %}>{{ option[1] }}</option>
          {% endfor %}
        </select>
      </div>
      <div class="alert alert-danger" id='public-visible-warning' data-module="warning-display">
        By putting visibility to public, the dataset entry will become publicly available to anyone visiting this website.
      </div>
*/

Instructions
============
------------------------------------------------
To Update the Meta Data in the project, you need to update the [dataset-schema.json](../src/ckanext-data-catalog-510/ckanext/data_catalog_510/dataset-schema.json)

The schema file consist of two items:-

#### `dataset_fields`, `resource_fields`

```json
{
  "dataset_fields": [
    {
      "field_name": "title",
      "label": "Title",
      "preset": "title"
    },
    {
      "field_name": "name",
      "label": "URL",
      "preset": "dataset_slug"
    }
  ],
  "resource_fields": [
    {
      "field_name": "url",
      "label": "URL",
      "preset": "resource_url_upload"
    },
    {
      "field_name": "name",
      "label": "Name",
      "form_placeholder": "gold_price.csv"
    }
  ]
}
```

Fields are specified in the order you
would like them to appear in the dataset and resource editing
pages.

Fields you exclude will not be shown to the end user, and will not
be accepted when editing or updating this type of dataset.

For more details on how to setup the fields please follow [ckanext-scheming](https://github.com/ckan/ckanext-scheming/)

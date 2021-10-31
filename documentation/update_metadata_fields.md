# Instructions

---

To Update the Meta Data Fields in the project, you need to update the [dataset-schema.json](../src/ckanext-data-catalog-510/ckanext/data_catalog_510/dataset-schema.json)

The schema file sample:-

#### `dataset_fields`

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
  ]
}
```

Fields are specified in the order you
would like them to appear in the dataset and resource editing
pages.

Fields you exclude will not be shown to the end user, and will not
be accepted when editing or updating this type of dataset.

For more details on how to setup the fields please follow [ckanext-scheming](https://github.com/ckan/ckanext-scheming/)

**Note:- The resource section is handled by [custom UI components](../src/ckanext-data-catalog-510/datapub-510-custom-ui/README.md), so the scheming section cannot be reused.**

### Developer's Notes

There are some items that are extended from the `ckanext-scheming` templates for desired results, please check those in [scheming templates directory](../src/ckanext-data-catalog-510/ckanext/data_catalog_510/templates/scheming)

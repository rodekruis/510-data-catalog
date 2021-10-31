# Developer's Guide

The CKAN installation is based on the `docker-compose setup`, follow project [README](../README.md) for the setup

## Components Used

The project is dependent on the below extensions, so follow the guide of extensions for any extension related item

- [ckanext-developerpage](https://github.com/datopian/ckanext-developerpage.git)
- [ckanext-envvars](https://github.com/okfn/ckanext-envvars.git)
- [ckanext-scheming](https://github.com/ckan/ckanext-scheming.git)
- [ckanext-saml2auth](https://github.com/keitaroinc/ckanext-saml2auth.git)
- [ckanext-spatial](https://github.com/ckan/ckanext-spatial.git)
- [ckanext-geoview](https://github.com/ckan/ckanext-geoview.git)
- [ckanext-harvest](https://github.com/ckan/ckanext-harvest.git)
- [ckanext-datapub](https://github.com/datopian/ckanext-datapub)

## Patches

There are some patch created for the CKAN and the extension that is required for the proper functioning of the project and is available at [ckan-patch](../ckan-build/ckan-service/patches) and [extension-patch](../ckan-build/ckan-service/patch_extensions). So if any change is required in the `community extensions` and `ckan base`, new patches can be created and added with `.patch` extension. To create the patch modify the code and create a `.patch` file from the diff
e.g. `git diff file > filename.patch` and place it in above-mentioned directories accordingly.

## 510 Extension

The Extension is created by following the [extension guide](https://docs.ckan.org/en/2.9/extensions/index.html) by ckan.

### Dependencies

The Extension is dependent on the PyPI packages that are added to the [requirements.txt](../src/ckanext-data-catalog-510/requirements.txt)

So while developing if a new package is required that need to be added to [requirements.txt](../src/ckanext-data-catalog-510/requirements.txt) to make the functioning smooth.

### Custom UI

The Custom UI is used to Resource Create and Resource Edit setup for the Databases, Data lake, and External links. This UI is built over `Angular 12`. Please follow the [documentation](../src/ckanext-data-catalog-510/datapub-510-custom-ui/README.md) for the usage and implementation of the UI.
The custom UI is based on the logic of [datapub extension](https://github.com/datopian/ckanext-datapub)

Whenever you change something in the Custom UI you need to rebuild the artifacts, so to do that

- Go to `src/ckanext-data-catalog-510/` directory
- Run command `./sync.sh ./datapub-510-custom-ui`.
- It will update the assets in `src/ckanext-data-catalog-510/ckanext/data_catalog_510/assets`. It will update both JS and CSS files
- It is used by the file `src/ckanext-data-catalog-510/ckanext/data_catalog_510/templates/datapub/snippets/resource_module.html`

This way you can implement your custom UI changes to the 510 Data Catalog Project

### Important Links and commands

- For [CKAN configuration](https://docs.ckan.org/en/2.9/maintaining/configuration.html)
- For [Environment Variables](https://github.com/okfn/ckanext-envvars/blob/master/README.rst)
- If you change anything in DB directly or you want to recover broken solr, please run the following:-
      - Log in to the pod/container
      - Run the following command `ckan search-index rebuild`
- To Create a user as sysadmin `ckan sysadmin add <username>`
- You can find more ckan commands [here](https://docs.ckan.org/en/2.9/maintaining/cli.html)
- CKAN API [Guide](https://docs.ckan.org/en/2.9/api/index.html)
- CKAN Theming [Guide](https://docs.ckan.org/en/2.9/theming/index.html)
- For Customizing CKAN Look and feel by Admin [Guide](https://docs.ckan.org/en/2.9/sysadmin-guide.html#customizing-look-and-feel)

### Tests

- CKAN tests are running on the Github [workflow](../.github/workflows/main.yml)
- To Get the tests result you can go to [Github Actions](https://github.com/rodekruis/510-data-catalog/actions) and click on the workflow with your commit message.
- You will see a Job with `test` written, click on that.
- Click on the stage `Run Tests`.
- You will see how many tests are passed and failed.

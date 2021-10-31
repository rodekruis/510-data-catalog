# 510 Custom UI on Angular for CKAN Resource on [Datapub](https://github.com/datopian/datapub) methodology

## Project Structure

```
├── README.md
├── angular.json
├── dist
│   └── test-app
├── karma.conf.js
├── package.json
├── src
│   ├── app
│   │   ├── app.component.css
│   │   ├── app.component.html
│   │   ├── app.component.spec.ts
│   │   ├── app.component.ts
│   │   ├── app.module.ts
│   │   ├── common
│   │   │   ├── common.module.ts
│   │   │   ├── components
│   │   │   │   ├── alert
│   │   │   │   │   ├── alert.component.css
│   │   │   │   │   ├── alert.component.html
│   │   │   │   │   ├── alert.component.spec.ts
│   │   │   │   │   └── alert.component.ts
│   │   │   │   ├── index.ts
│   │   │   │   └── validations
│   │   │   │       ├── validation.component.css
│   │   │   │       ├── validation.component.html
│   │   │   │       ├── validation.component.spec.ts
│   │   │   │       └── validation.component.ts
│   │   │   ├── constant.ts
│   │   │   └── services
│   │   │       ├── alert.service.spec.ts
│   │   │       ├── alert.service.ts
│   │   │       ├── common.service.spec.ts
│   │   │       ├── common.service.ts
│   │   │       ├── interceptor.service.spec.ts
│   │   │       └── interceptor.service.ts
│   │   ├── databases
│   │   │   ├── databases.component.css
│   │   │   ├── databases.component.html
│   │   │   ├── databases.component.spec.ts
│   │   │   └── databases.component.ts
│   │   ├── datalake
│   │   │   ├── datalake.component.css
│   │   │   ├── datalake.component.html
│   │   │   ├── datalake.component.spec.ts
│   │   │   └── datalake.component.ts
│   │   ├── datalake-browser
│   │   │   ├── datalake-browser.component.css
│   │   │   ├── datalake-browser.component.html
│   │   │   ├── datalake-browser.component.spec.ts
│   │   │   └── datalake-browser.component.ts
│   │   └── link
│   │       ├── link.component.css
│   │       ├── link.component.html
│   │       ├── link.component.spec.ts
│   │       └── link.component.ts
│   ├── assets
│   ├── environments
│   │   ├── environment.prod.ts
│   │   └── environment.ts
│   ├── favicon.ico
│   ├── index.html
│   ├── main.ts
│   ├── polyfills.ts
│   ├── styles.css
│   └── test.ts
├── tsconfig.app.json
├── tsconfig.json
├── tsconfig.spec.json
└── yarn.lock
```

The Project is built over Angular 12.

### Installation

```shell
yarn install
yarn start
```

### Components

There are 4 main components that are used in the project:

1. Link Component
2. Database Component
3. Datalake Component
4. Datalake Browser Component

#### Link Component

- The component is used to create and edit the resource which is having a URL for the external website or maybe a URL for internal.
- The Link Component uses the `ckan` API's like `resource_show`, `resource_create` etc
- The `package_patch` API is used to make the dataset state is active when the dataset is being created the first time.
- The `resource_show` API is used to fetch the resource data to prefill the form for using the edit functionality

#### Database Component

- Database Component is used to create the resource on the basis of selection made for the type of database, schema, and table.
- The Component is used for fetching the Database Type and details and to auto-populate the metadata field and try to auto check that whether the type of data is `geo` data or not.
- The component contains the field to fill for the geo_metadata on the basis `is_geo` key or the checkbox in the UI
- The `package_patch` API is used to make the dataset state is active when the dataset is being created the first time.
- The `resource_show` API is used to fetch the resource data to prefill the form for using the edit functionality

#### Datalake Component

- Datalake Component is used to create the resource on the selection of the directory/file from the datalake which is fetched using the [Datalake Browser Component](#datalake-browser-component)
- The Component is used for fetching the Database Type and details and to auto-populate the metadata field and try to auto check that whether the type of data is `geo` data or not.
- The component contains the field to fill for the geo_metadata on the basis `is_geo` key or the checkbox in the UI
- The `package_patch` API is used to make the dataset state is active when the dataset is being created the first time.
- The `resource_show` API is used to fetch the resource data to prefill the form for using the edit functionality

#### Datalake Browser Component

- Datalake browser component is used to fetch and create a UI to browser the Containers/Directories/Files
- It helps to Select the selection you made while browsing and prefill the `No of Files` Section in the [Datalake Component](#datalake-component)

#### Logic

- The tag `<app-root>` is being extended to input three values:
  - `pkg_name` - The name of the dataset/package where resources needs to be added/updated
  - `res` - The resource name in case of edit
  - `type` - Type of call either e.g. `edit`

- On the basis of the above inputs the UI is shown from `app-component`.
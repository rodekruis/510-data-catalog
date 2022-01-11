import { Component, OnInit, Input } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { commonService } from 'src/app/common/services/common.service';
import { AlertService } from 'src/app/common/services/alert.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import Swal from 'sweetalert2';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-databases',
  templateUrl: './databases.component.html',
  styleUrls: ['./databases.component.css'],
})
export class DatabasesComponent implements OnInit {
  base_url;
  API_LIST = {
    get_all_dbs: '/api/3/action/get_all_dbs',
    get_databases_connections: '/api/3/action/get_db_connections',
    get_schemas: '/api/3/action/get_schemas',
    get_tables: '/api/3/action/get_tables',
    get_table_metadata: '/api/3/action/get_tables_metadata',
    resource_create: '/api/3/action/resource_create',
    resource_patch: '/api/3/action/resource_patch',
    resource_show: '/api/3/action/resource_show',
    package_show: '/api/3/action/package_show',
    package_patch: '/api/3/action/package_patch',
    check_db_credentials: '/api/3/action/check_db_credentials',
    package_ext_spatial_patch: '/api/3/action/package_ext_spatial_patch'
  };
  headers = {
    Accept: 'application/json',
  };
  databaseForm: FormGroup;
  allDatabasesType: Array<{ name: ''; title: '' }> = [];
  selectedDBType: string = '';
  dbConnections: Array<{ name: ''; title: '' }> = [];
  selectedConnection: string = '';
  dbSchemas: Array<[]> = [];
  selectedSchema: string = '';
  tables: Array<[]> = [];
  metaData: any = {};
  is_geo: boolean = false;
  resource_data: any;
  dbLogin: boolean;
  loadValue: boolean;
  token: string = null;
  @Input() pkg_name: any;
  @Input() type: any;
  @Input() resource: any;
  constructor(
    private commonService: commonService,
    private http: HttpClient,
    private alertService: AlertService
  ) {
    this.base_url = environment.base_url;
    this.dbLogin = false;
    this.loadValue = true;
    this.databaseForm = new FormGroup({
      database_connection_type: new FormControl(
        '',
        Validators.compose([Validators.required])
      ),
      database_connection: new FormControl('', [Validators.required]),
      schema_name: new FormControl('', [Validators.required]),
      table_name: new FormControl('', [Validators.required]),
      metadata: new FormGroup({
        no_of_records: new FormControl(''),
        no_of_attributes: new FormControl(''),
      }),
      geo_metadata: new FormGroup({
        spatial_resolution: new FormControl(''),
        temporal_resolution: new FormControl(''),
        spatial_extent: new FormControl(''),
        temporal_extent: new FormControl(''),
        spatial_reference_system: new FormControl(''),
      }),
      name: new FormControl('', [Validators.required]),
      description: new FormControl('', [Validators.required]),
      format: new FormControl(''),
    });
  }

  ngOnInit() {
    this.getAllDatabasesType();
  }

  get f() {
    return this.databaseForm.controls;
  }

  clearSelects(type) {
    if (type == 'database_type') {
      this.dbConnections = [];
      this.dbSchemas = [];
      this.tables = [];
      this.token = null;
      this.databaseForm.patchValue({
        database_connection: '',
        schema_name: '',
        table_name: '',
        metadata: {
          no_of_records: '',
          no_of_attributes: '',
        },
        geo_metadata: {
          spatial_resolution: '',
          temporal_resolution: '',
          spatial_extent: '',
          temporal_extent: '',
          spatial_reference_system: '',
        },
      });
    }
    if (type == 'connections') {
      this.dbSchemas = [];
      this.tables = [];
      this.token = null;
      this.databaseForm.patchValue({
        database_connection: '',
        schema_name: '',
        table_name: '',
        metadata: {
          no_of_records: '',
          no_of_attributes: '',
        },
        geo_metadata: {
          spatial_resolution: '',
          temporal_resolution: '',
          spatial_extent: '',
          temporal_extent: '',
          spatial_reference_system: '',
        },
      });
    }
    if (type == 'schema') {
      this.tables = [];
      this.databaseForm.patchValue({
        schema_name: '',
        table_name: '',
        metadata: {
          no_of_records: '',
          no_of_attributes: '',
        },
        geo_metadata: {
          spatial_resolution: '',
          temporal_resolution: '',
          spatial_extent: '',
          temporal_extent: '',
          spatial_reference_system: '',
        },
      });
    }
    if (type == 'table') {
      this.databaseForm.patchValue({
        table_name: '',
        metadata: {
          no_of_records: '',
          no_of_attributes: '',
        },
        geo_metadata: {
          spatial_resolution: '',
          temporal_resolution: '',
          spatial_extent: '',
          temporal_extent: '',
          spatial_reference_system: '',
        },
      });
    }
  }

  getAllDatabasesType() {
    this.commonService.showLoader = true;
    this.http
      .post<any>(
        this.base_url + this.API_LIST.get_all_dbs,
        {},
        {
          headers: this.headers,
        }
      )
      .subscribe(
        (res) => {
          this.commonService.showLoader = false;
          this.allDatabasesType = res.result;
          this.clearSelects('database_type');
          if (this.type == 'edit') {
            this.getResource();
          }
        },
        (error) => {
          this.alertService.error(error?.error?.error?.message);
          this.commonService.showLoader = false;
        }
      );
  }

  async openDbLogin(db_name, db_type) {
    // console.log(db_name);
    let status = false;
    status = await Swal.fire({
      title: `Login to ${db_type}/${db_name}`,
      html: `<input type="text" id="login" class="swal2-input" placeholder="Username">
      <input type="password" id="password" class="swal2-input" placeholder="Password">`,
      confirmButtonText: 'Sign in',
      focusConfirm: false,
      preConfirm: () => {
        const login = (Swal.getPopup().querySelector('#login') as HTMLInputElement).value;
        const password = (Swal.getPopup().querySelector('#password') as HTMLInputElement).value;
        if (!login || !password) {
          Swal.showValidationMessage(`Please enter login and password`)
        }
        return { username: login, password: password }
      }
    }).then(async (result) => {
      if(result.value) {
        let token = btoa(result.value.username + ':' + result.value.password)
        let isLoggedIn: boolean = await this.checkDbLogin(db_name, db_type, token);
        // console.log(isLoggedIn);
        if(isLoggedIn) {
          this.token = token;
          return Swal.fire('Success!', 'Your credentials have been validated.', 'success').then((result) => { return true; });
        } else {
          return Swal.fire('Invalid!', 'Your credentials are invalid.', 'error').then((result) => { return false; });
        }
      } else {
        return false;
      }
    })
    return status;
  }

  checkDbLogin(db_name, db_type, token) {
    let data = {
      db_name: db_name,
      db_type: db_type,
      token: token,
    }

    return this.http
    .post<any>(this.base_url + this.API_LIST.check_db_credentials, data, { headers: this.headers })
    .toPromise()
    .then((res) => {
      if(res.result) {
        return res.result;
      }
    })
    .catch((error) => {
      this.alertService.error(error?.error?.error?.message);
      return false;
    })
  }

  selectDatabase(db_type) {
    if (db_type == '') {
      return;
    }
    this.commonService.showLoader = true;
    let data = {
      db_type,
    };
    this.http
      .post<any>(
        this.base_url + this.API_LIST.get_databases_connections,
        data,
        {
          headers: this.headers,
        }
      )
      .subscribe(
        (res) => {
          this.commonService.showLoader = false;
          this.dbConnections = res.result;
          this.selectedDBType = db_type;
          this.clearSelects('connections');
          // console.log(this.loadValue);
          if (this.type == 'edit' && this.loadValue) {
            this.selectSchema(this.resource_data.database_connection);
          }
        },
        (error) => {
          this.alertService.error(error?.error?.error?.message);
          this.commonService.showLoader = false;
        }
      );
  }

  async selectSchema(db_name) {
    if (db_name == '') {
      return;
    }
    // console.log(this.selectedDBType);
    let loggedIn: boolean;
    if(this.type != "edit") {
      this.loadValue = false;
    }
    if(this.selectedDBType !== 'azuresql' && !this.loadValue) {
      loggedIn = await this.openDbLogin(db_name, this.selectedDBType);
    } else { loggedIn = true; }
    if(!loggedIn) {
      this.clearSelects('connections');
    } else {
      this.commonService.showLoader = true;
      this.selectedConnection = db_name;
      let data = {
        db_type: this.selectedDBType,
        db_name,
        token: this.token
      };
      this.http
        .post<any>(this.base_url + this.API_LIST.get_schemas, data, {
          headers: this.headers,
        })
        .subscribe(
          (res) => {
            this.commonService.showLoader = false;
            this.dbSchemas = res.result;
            this.clearSelects('schema');
            if (this.type == 'edit') {
              this.selectTable(this.resource_data.schema_name);
            }
          },
          (error) => {
            this.alertService.error(error?.error?.error?.message);
            this.commonService.showLoader = false;
          }
        );
    }
  }

  async selectTable(schema) {
    this.selectedSchema = schema;
    if (schema == '') {
      return;
    }
    let loggedIn: boolean;
    if( !this.token && this.selectedDBType !== 'azuresql' && !this.loadValue) {
      loggedIn = await this.openDbLogin(this.selectedConnection, this.selectedDBType);
    } else {
      loggedIn = true;
    }
    if(!loggedIn) {
      this.clearSelects('schema');
    } else {
      this.commonService.showLoader = true;
      let data = {
        db_type: this.selectedDBType,
        db_name: this.selectedConnection,
        schema,
        token: this.token
      };
      this.http
        .post<any>(this.base_url + this.API_LIST.get_tables, data, {
          headers: this.headers,
        })
        .subscribe(
          (res) => {
            this.commonService.showLoader = false;
            this.tables = res.result;
            if(this.type === "edit" && this.loadValue) {
              this.databaseForm.patchValue(this.resource_data);
              this.loadValue = false;
            }
          },
          (error) => {
            this.tables = [];
            this.alertService.error(error?.error?.error?.message);
            this.commonService.showLoader = false;
          }
        );
      }
  }

  getResource() {
    this.http
      .post<any>(
        this.base_url + this.API_LIST.resource_show,
        { id: this.resource },
        {
          headers: this.headers,
        }
      )
      .subscribe(
        (res) => {
          this.commonService.showLoader = false;
          this.resource_data = res?.result;
          Object.values(this.resource_data.geo_metadata).forEach(element => { if (element != "" || element != undefined) this.is_geo = true });
          if (this.type == 'edit') {
            this.selectDatabase(this.resource_data.database_connection_type);
          }
        },
        (error) => {
          this.alertService.error(error?.error?.error?.message);
          this.commonService.showLoader = false;
        }
      );
  }

  async selectMetaData(table) {
    if (table == '') {
      return;
    }
    let loggedIn: boolean;
    if(!this.token && this.selectedDBType !== 'azuresql' && !this.loadValue) {
      loggedIn = await this.openDbLogin(this.selectedConnection, this.selectedDBType);
    } else {
      loggedIn = true;
    }
    if(loggedIn) {
      this.commonService.showLoader = true;
      let data = {
        db_type: this.selectedDBType,
        db_name: this.selectedConnection,
        schema: this.selectedSchema,
        table,
        token: this.token,
      };
      this.http
        .post<any>(this.base_url + this.API_LIST.get_table_metadata, data, {
          headers: this.headers,
        })
        .subscribe(
          (res) => {
            this.commonService.showLoader = false;
            this.metaData = res.result;
            // console.log(this.metaData)
            if (this.metaData?.is_geo == true) {
              this.is_geo = true;
              this.databaseForm.patchValue({
                geo_metadata: {
                  spatial_extent: this.metaData.geo_metadata.spatial_extent,
                  spatial_resolution: this.metaData.geo_metadata.spatial_resolution,
                  spatial_reference_system: this.metaData.geo_metadata.spatial_reference_system
                }
              })
            }
            this.databaseForm.patchValue({
              metadata: {
                no_of_records: this.metaData.no_of_records,
                no_of_attributes: this.metaData.no_of_attributes,
              },
              format: this.metaData.format
            });
          },
          (error) => {
            this.alertService.error(error?.error?.error?.message);
            this.commonService.showLoader = false;
          }
        );
      } else {
        this.clearSelects('table');
      }
  }

  addSpatialExtra(id) {
    let data = {
      id,
      spatial_extent: this.databaseForm.get('geo_metadata').get('spatial_extent').value
    }
    // console.log(data)
    this.http.post<any>(this.base_url + this.API_LIST.package_ext_spatial_patch, data, {headers:this.headers})
    .subscribe((res) => {
      // console.log(res.result)
    }, (error) => {
      this.alertService.error(error?.error?.error?.message);
    })
  }

  handleDraftPackage(id) {
    let data = {
      id,
    };

    this.http
      .post<any>(this.base_url + this.API_LIST.package_show, data, {})
      .subscribe(
        (res) => {
          this.commonService.showLoader = false;
          if (res.result.state == 'draft') {
            let update_data = { id, state: 'active' };
            this.http
              .post<any>(
                this.base_url + this.API_LIST.package_patch,
                update_data,
                {
                  headers: this.headers,
                }
              )
              .subscribe(
                (res) => {},
                (error) => {
                  this.alertService.error(error?.error?.error?.message);
                }
              );
          }
        },
        (error) => {
          this.alertService.error(error?.error?.error?.message);
          this.commonService.showLoader = false;
        }
      );
  }

  submit() {
    let api_url = this.API_LIST.resource_create;
    if (!this.databaseForm.valid) {
      return this.commonService.validateAllFormFields(this.databaseForm);
    }
    if (this.is_geo == true) {
      let geoMetadata = this.databaseForm.get('geo_metadata');
      this.databaseForm.patchValue({
        geo_metadata: geoMetadata?.value,
      });
    }
    let data = {
      package_id: this.pkg_name,
      ...this.databaseForm.value,
      resource_type: 'database',
    };
    if (this.type == 'edit') {
      api_url = this.API_LIST.resource_patch;
      data['id'] = this.resource;
    }
    this.handleDraftPackage(this.pkg_name);
    if(this.is_geo) {
      this.addSpatialExtra(this.pkg_name);
    }
    this.commonService.showLoader = true;
    this.http.post<any>(this.base_url + api_url, data, {}).subscribe(
      (res) => {
        this.commonService.showLoader = false;
        let message;
        if (this.type == 'edit') {
          message = 'Resource Updated Successfully';
        } else {
          message = 'Resource Created Successfully';
        }
        Swal.fire({
          icon: 'success',
          text: message,
        }).then((result) => {
          window.location.assign(
            window.location.origin + '/dataset/' + res?.result?.package_id
          );
        });
      },
      (error) => {
        this.alertService.error(error?.error?.error?.message);
        this.commonService.showLoader = false;
      }
    );
  }
}

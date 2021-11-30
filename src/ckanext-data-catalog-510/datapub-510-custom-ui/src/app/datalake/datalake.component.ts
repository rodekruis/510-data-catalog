import { Component, OnInit, Input } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { URL_PATTERN } from 'src/app/common/constant';
import { commonService } from 'src/app/common/services/common.service';
import { AlertService } from 'src/app/common/services/alert.service';
import Swal from 'sweetalert2';

import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-datalake',
  templateUrl: './datalake.component.html',
  styleUrls: ['./datalake.component.css'],
})

export class DatalakeComponent implements OnInit {
  base_url;
  API_LIST = {
    resource_create: '/api/3/action/resource_create',
    resource_patch: '/api/3/action/resource_patch',
    resource_show: '/api/3/action/resource_show',
    package_show: '/api/3/action/package_show',
    package_patch: '/api/3/action/package_patch',
    get_geo_metadata: '/api/3/action/get_geo_metadata',
    get_directories_and_files: '/api/3/action/get_directories_and_files'
  };
  headers = {
    Accept: 'application/json',
  };
  datalakeForm: FormGroup;
  @Input() pkg_name: any;
  @Input() type: any;
  @Input() resource: any;
  resourceData;
  resourceSelected;
  no_of_files;
  list_of_files = [];
  selectedBaseFilePath: string = null;
  is_geo;
  geo_metadata: any = {}
  fetchDatalake: boolean = false;

  constructor(
    private commonService: commonService,
    private http: HttpClient,
    private alertService: AlertService
  ) {
    this.base_url = environment.base_url;
    this.datalakeForm = new FormGroup({
      name: new FormControl('', [Validators.required]),
      geo_metadata: new FormGroup({
        spatial_resolution: new FormControl(''),
        temporal_resolution: new FormControl(''),
        spatial_extent: new FormControl(''),
        temporal_extent: new FormControl(''),
        spatial_reference_system: new FormControl(''),
      }),
      description: new FormControl('', [Validators.required]),
      format: new FormControl(''),
      datalake_data: new FormControl(''),
    });
  }

  ngOnInit(): void {
    if (this.type == 'edit') {
      this.getResource();
    }
    this.selectedBaseFilePath = null
  }

  get f() {
    return this.datalakeForm.controls;
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
          this.resourceData = res.result;
          if (this.resourceData?.geo_metadata) {
            this.is_geo = true;
          }
          this.datalakeForm.patchValue({
            name: this.resourceData?.name,
            description: this.resourceData?.description,
            geo_metadata: this.resourceData?.geo_metadata,
            format: this.resourceData?.format,
            datalake_data: this.resourceData?.datalake_data,
          });
          this.resourceSelected = `${this.resourceData?.datalake_data?.container}/${this.resourceData?.datalake_data?.file_path}`;
          this.getListOfFiles(this.resourceData?.datalake_data)
        },
        (error) => {
          this.alertService.error(error?.error?.error?.message);
          this.commonService.showLoader = false;
        }
      );
  }

  selectedResource(value) {
    this.fetchDatalake = !this.fetchDatalake;
    this.resourceSelected = `${value.container}/${value.file_path}`;
    if (value.type != 'file') {
      this.no_of_files = value.no_of_files;
    }
    this.datalakeForm.patchValue({ name: value.file_path.split('/').pop() });
    this.datalakeForm.patchValue({ datalake_data: value });
    // console.log(value);
    this.getListOfFiles(value)
  }

  getListOfFiles(value) {
    this.http.post<any>(this.API_LIST.get_directories_and_files,
      {
        container: value.container,
        path: value.file_path
      },
      {
        headers: this.headers
      }).subscribe((res) => {
        if (res.result) {
          this.list_of_files = []
          for (let i = 0; i < res.result['directory_structure'].length; i++) {
            if (res.result['directory_structure'][i]['type'] === "file") {
              this.list_of_files.push(res.result['directory_structure'][i]['path'])
            }
          }
        }
      }, (error) => {
        this.alertService.error(error?.error?.error?.message);
      })
    this.selectedBaseFilePath = null
  }

  getGeoMetadata() {
    if (this.is_geo) {
      Swal.fire({
        title: "Auto-fill spatial metadata?",
        text: "To auto-fill, we will download the file to our servers. This process may take time. Please reconsider if the file is big.",
        showCancelButton: true,
        confirmButtonText: "Continue",
      }).then((result) => {
        if (result.isConfirmed) {
          let [container, ...path] = this.resourceSelected.split('/')
          // console.log(container, path.join('/'))
          let data = {
            container: container,
            // 'path': path.join('/')
            path: this.selectedBaseFilePath
          }
          // console.log(data)
          this.commonService.showLoader = true;
          this.http.post<any>(this.base_url + this.API_LIST.get_geo_metadata, data, {})
            .subscribe((res) => {
              this.commonService.showLoader = false;
              // console.log(res.result)
              if (res.result) {
                this.datalakeForm.patchValue({
                  geo_metadata: {
                    spatial_resolution: res.result['spatial_resolution'],
                    spatial_extent: res.result['spatial_extent'],
                    spatial_reference_system: res.result['spatial_reference_system']
                  }
                });
              }
            }, (error) => {
              this.alertService.error(error?.error?.error?.message);
              this.commonService.showLoader = false;
            });
        }
      });
    }
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
                (res) => { },
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
    if (!this.datalakeForm.valid) {
      return this.commonService.validateAllFormFields(this.datalakeForm);
    }
    if (this.is_geo == true) {
      let geoMetadata = this.datalakeForm.get('geo_metadata');
      this.datalakeForm.patchValue({
        geo_metadata: geoMetadata?.value,
      });
    }
    let data = {
      package_id: this.pkg_name,
      ...this.datalakeForm.value,
      resource_type: 'datalake',
    };
    if (this.type == 'edit') {
      api_url = this.API_LIST.resource_patch;
      data['id'] = this.resource;
    }
    this.handleDraftPackage(this.pkg_name);
    this.commonService.showLoader = true;
    this.http
      .post<any>(this.base_url + api_url, data, {
        headers: this.headers,
      })
      .subscribe(
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

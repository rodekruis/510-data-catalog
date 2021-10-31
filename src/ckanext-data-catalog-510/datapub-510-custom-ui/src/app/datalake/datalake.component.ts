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
  };
  headers = {
    Accept: 'application/json',
    Authorization:
      'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlSS04UUxyYVR6eUtyZHJmQl9PNmlIdVlRYnhKdWN1S05JWWtFYkVLcXBGRkdSMng5NkpUVXRiLXh5UkVSUW9QQVhSOURVM1lobHhtbF9kMSIsImlhdCI6MTYzNTY4Mzc3MH0.zI18LG9oq3bL6cJaAkrv74N1Bx0t72cy8-Ih3GtWHns',
  };
  datalakeForm: FormGroup;
  @Input() pkg_name: any;
  @Input() type: any;
  @Input() resource: any;
  resourceData;
  resourceSelected;
  no_of_files;
  fetchDatalake: boolean = false;

  constructor(
    private commonService: commonService,
    private http: HttpClient,
    private alertService: AlertService
  ) {
    this.base_url = environment.base_url;
    this.datalakeForm = new FormGroup({
      name: new FormControl('', [Validators.required]),
      description: new FormControl('', [Validators.required]),
      format: new FormControl(''),
      datalake_data: new FormControl(''),
    });
  }

  ngOnInit(): void {
    if (this.type == 'edit') {
      this.getResource();
    }
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
          this.datalakeForm.patchValue({
            name: this.resourceData?.name,
            description: this.resourceData?.description,
            format: this.resourceData?.format,
            datalake_data: this.resourceData?.datalake_data,
          });
          this.resourceSelected = `${this.resourceData?.datalake_data?.container}/${this.resourceData?.datalake_data?.file_path}`;
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
    if (!this.datalakeForm.valid) {
      return this.commonService.validateAllFormFields(this.datalakeForm);
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
        headers: { Authorization: '' },
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

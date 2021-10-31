import { Component, OnInit, Input } from '@angular/core';
import {
  FormGroup,
  FormControl,
  Validators,
  FormBuilder,
} from '@angular/forms';
import { URL_PATTERN } from 'src/app/common/constant';
import { commonService } from 'src/app/common/services/common.service';
import { AlertService } from 'src/app/common/services/alert.service';
import Swal from 'sweetalert2';

import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-link',
  templateUrl: './link.component.html',
  styleUrls: ['./link.component.css'],
})
export class LinkComponent implements OnInit {
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
  };
  linkForm: FormGroup;
  @Input() pkg_name: any;
  @Input() type: any;
  @Input() resource: any;
  resourceData;

  constructor(
    private commonService: commonService,
    private http: HttpClient,
    private alertService: AlertService
  ) {
    this.base_url = environment.base_url;
    this.linkForm = new FormGroup({
      url: new FormControl(
        '',
        Validators.compose([
          Validators.required,
          Validators.pattern(URL_PATTERN),
        ])
      ),
      name: new FormControl('', [Validators.required]),
      description: new FormControl('', [Validators.required]),
      format: new FormControl(''),
    });
  }

  ngOnInit(): void {
    if (this.type == 'edit') {
      this.getResource();
    }
  }

  get f() {
    return this.linkForm.controls;
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
          this.linkForm.patchValue({
            url: this.resourceData?.url,
            name: this.resourceData?.name,
            description: this.resourceData?.description,
            format: this.resourceData?.format,
          });
        },
        (error) => {
          this.alertService.error(error?.error?.error?.message);
          this.commonService.showLoader = false;
        }
      );
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
    if (!this.linkForm.valid) {
      return this.commonService.validateAllFormFields(this.linkForm);
    }

    let data = {
      package_id: this.pkg_name,
      ...this.linkForm.value,
      resource_type: 'url',
    };
    if (this.type == 'edit') {
      api_url = this.API_LIST.resource_patch;
      data['id'] = this.resource;
    }
    this.handleDraftPackage(this.pkg_name);
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

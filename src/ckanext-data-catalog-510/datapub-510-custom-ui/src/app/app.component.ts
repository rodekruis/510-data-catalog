import { Component, Input, OnInit, ElementRef } from '@angular/core';
import { commonService } from './common/services/common.service';

import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
  base_url;
  isLink: any = false;
  isDatabase: any = false;
  isDatalake: any = false;
  package_id: any;
  resource: any;
  type: any;
  isDisabled;
  constructor(
    private elementRef: ElementRef,
    public commonService: commonService,
    private http: HttpClient
  ) {
    this.base_url = environment.base_url;
    this.package_id = this.elementRef.nativeElement.getAttribute('pkg_name');
    this.resource = this.elementRef.nativeElement.getAttribute('res');
    this.type = this.elementRef.nativeElement.getAttribute('type');
  }
  ngOnInit(): void {
    this.getResource();
  }

  getResource() {
    this.http
      .post<any>(
        this.base_url + '/api/3/action/resource_show',
        { id: this.resource },
        {
          headers: {
            Accept: 'application/json',
          },
        }
      )
      .subscribe(
        (res) => {
          this.commonService.showLoader = false;
          if (res.result.resource_type == 'url') {
            this.switchTab('link');
          } else if (res.result.resource_type == 'database') {
            this.switchTab('database');
          } else if (res.result.resource_type == 'datalake') {
            this.switchTab('datalake');
          } else {
            this.switchTab('link');
          }

          if (this.type == 'edit') {
            this.isDisabled = true;
          }
        },
        (error) => {
          this.commonService.showLoader = false;
        }
      );
  }
  switchTab(type: string): void {
    if (type == 'link') {
      this.isLink = true;
      this.isDatabase = false;
      this.isDatalake = false;
    }
    if (type == 'database') {
      this.isLink = false;
      this.isDatabase = true;
      this.isDatalake = false;
    }
    if (type == 'datalake') {
      this.isLink = false;
      this.isDatabase = false;
      this.isDatalake = true;
    }
  }
}

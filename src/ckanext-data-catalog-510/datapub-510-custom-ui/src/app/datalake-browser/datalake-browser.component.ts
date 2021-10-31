import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { commonService } from 'src/app/common/services/common.service';
import { AlertService } from 'src/app/common/services/alert.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import Swal from 'sweetalert2';
import { environment } from 'src/environments/environment';
@Component({
  selector: 'app-datalake-browser',
  templateUrl: './datalake-browser.component.html',
  styleUrls: ['./datalake-browser.component.css'],
})
export class DatalakeBrowserComponent implements OnInit {
  @Output() selectedDatalakeResource = new EventEmitter();
  base_url;
  API_LIST = {
    get_containers: '/api/3/action/get_containers',
    get_directories_and_file: '/api/3/action/get_directories_and_files',
    get_no_of_files: '/api/3/action/get_no_of_files',
  };
  headers = {
    Accept: 'application/json',
    Authorization:
      'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlSS04UUxyYVR6eUtyZHJmQl9PNmlIdVlRYnhKdWN1S05JWWtFYkVLcXBGRkdSMng5NkpUVXRiLXh5UkVSUW9QQVhSOURVM1lobHhtbF9kMSIsImlhdCI6MTYzNTY4Mzc3MH0.zI18LG9oq3bL6cJaAkrv74N1Bx0t72cy8-Ih3GtWHns',
  };
  public containers: any[] = [];
  public files_and_directories: any[] = [];
  pageType: string = 'container';
  fileSelected: boolean = false;
  activeFile;
  prev_path;
  activeContainer;
  selectedFileDetails: any = {};
  no_of_files: any = 0;
  @Input() pkg_name: any;
  @Input() type: any;
  @Input() resource: any;
  constructor(
    private commonService: commonService,
    private http: HttpClient,
    private alertService: AlertService
  ) {
    this.base_url = environment.base_url;
  }

  ngOnInit(): void {
    this.getAllContainers();
  }

  getAllContainers() {
    this.commonService.showLoader = true;
    this.http
      .post<any>(
        this.base_url + this.API_LIST.get_containers,
        {},
        {
          headers: this.headers,
        }
      )
      .subscribe(
        (res) => {
          this.commonService.showLoader = false;
          this.pageType = 'container';
          this.containers = res.result;
        },
        (error) => {
          this.alertService.error(error?.error?.error?.message);
          this.commonService.showLoader = false;
        }
      );
  }

  selectFile(file) {
    this.getNoOfFiles(this.activeContainer, file?.path);
    this.fileSelected = true;
    this.selectedFileDetails = {
      container: this.activeContainer,
      file_path: file?.path,
      name: file?.name,
      type: file?.type,
      no_of_files: this.no_of_files,
    };
  }
  goToResourcePage() {
    this.selectedDatalakeResource.emit(this.selectedFileDetails);
  }
  cancel() {
    this.fileSelected = false;
    this.selectedFileDetails = {};
  }

  goBack() {
    if (this.prev_path == 'container') {
      this.getAllContainers();
    } else {
      this.getFiles(this.activeContainer, this.prev_path);
    }
  }
  getNoOfFiles(container, path) {
    let data = {
      container,
      path,
    };
    this.http
      .post<any>(this.base_url + this.API_LIST.get_no_of_files, data, {
        headers: this.headers,
      })
      .subscribe(
        (res) => {
          this.no_of_files = res.result;
        },
        (error) => {
          this.alertService.error(error?.error?.error?.message);
          this.commonService.showLoader = false;
        }
      );
  }

  getFiles(container, path) {
    this.fileSelected = false;
    this.pageType = 'files';
    this.commonService.showLoader = true;
    let data = {
      container,
      path,
    };
    this.http
      .post<any>(this.base_url + this.API_LIST.get_directories_and_file, data, {
        headers: this.headers,
      })
      .subscribe(
        (res) => {
          this.commonService.showLoader = false;
          if (res.result) {
            this.files_and_directories = res.result.directory_structure;
          } else {
            this.files_and_directories = [];
          }
          this.prev_path = res.result.prev_path;
          this.activeContainer = res.result.container;
        },
        (error) => {
          this.alertService.error(error?.error?.error?.message);
          this.commonService.showLoader = false;
        }
      );
  }
}

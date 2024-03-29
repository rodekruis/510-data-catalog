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
    get_datalake_file_search: "/api/3/action/get_datalake_file_search",
  };
  headers = {
    Accept: 'application/json',
  };
  public containers: any[] = [];
  public files_and_directories: any[] = [];
  pageType: string = 'container';
  fileSelected: boolean = false;
  activeFile;
  prev_path;
  activeContainer;
  currentDirectory = null;
  records_per_page: number = 5;
  selectedFileDetails: any = {};
  no_of_files: any = 0;
  totalRecords = 0;
  queryString: string;
  recordsOptions: number[] = [5, 10, 15]
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
    this.getCSRFToken();
    
    // this.getPageContainers(1);
  }

  private getCSRFToken(): void {
    const csrfMetaTag = document.querySelector('meta[name="_csrf_token"]');
    if (csrfMetaTag) {
      this.headers['X-CSRFToken'] = csrfMetaTag.getAttribute('content');
      this.getAllContainers();
    } 
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
          this.currentDirectory = null;
          this.containers = res.result;
        },
        (error) => {
          this.alertService.error(error?.error?.error?.message);
          this.commonService.showLoader = false;
        }
      );
  }

  getPageContainers(count) {
    this.commonService.showLoader = true;
    let data = {
      count,
    };
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
    this.no_of_files = null;
    this.getNoOfFiles(this.activeContainer, file?.path)
    .subscribe(
      (res) => {
        this.no_of_files = res.result;
        this.selectedFileDetails = {
          container: this.activeContainer,
          file_path: file?.path,
          name: file?.name,
          type: file?.type,
          no_of_files: this.no_of_files,
          format: file?.format
        };
      },
      (error) => {
        this.alertService.error(error?.error?.error?.message);
        this.commonService.showLoader = false;
      }
    );
    this.fileSelected = true;
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
      this.getFiles(this.activeContainer, this.prev_path, 1, this.records_per_page);
    }
  }
  
  getNoOfFiles(container, path) {
    let data = {
      container,
      path,
    };
    return this.http
      .post<any>(this.base_url + this.API_LIST.get_no_of_files, data, {
        headers: this.headers,
      });
  }

  getFiles(container, path, page_num, records_per_page) {
    this.fileSelected = false;
    this.pageType = 'files';
    this.commonService.showLoader = true;
    this.currentDirectory = '';
    let data = {
      container: container,
      path: path,
      page_num: page_num,
      records_per_page: parseInt(records_per_page)
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
            this.prev_path = res.result.prev_path;
            this.activeContainer = res.result.container;
            this.currentDirectory = path;
            this.totalRecords = res.result.total_records;
          } else {
            this.files_and_directories = [];
          }
        },
        (error) => {
          this.alertService.error(error?.error?.error?.message);
          this.commonService.showLoader = false;
        }
      );
  } 
  
  getPages(page_num) {
    this.fileSelected = false;
      this.pageType = 'files';
      this.commonService.showLoader = true;
      if(!this.queryString) {
      let data = {
        container: this.activeContainer,
        path: this.currentDirectory,
        page_num: page_num,
        records_per_page: this.records_per_page
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
          },
          (error) => {
            this.alertService.error(error?.error?.error?.message);
            this.commonService.showLoader = false;
          }
        );
      } else {
        this.getSearchResults(this.queryString, page_num);
      }
    }

  getSearchResults(query: string, page_num: number) {
    if(query) {
      this.queryString = query;
      this.commonService.showLoader = true;
      let data = {
        container: this.activeContainer,
        query: query,
        page_num: page_num,
        records_per_page: this.records_per_page
      }
      this.http.post<any>(this.base_url + this.API_LIST.get_datalake_file_search, data, { headers: this.headers })
      .subscribe(
        (res) => {
          this.files_and_directories = res.result.search_results;
          this.totalRecords = res.result.total_results;
          this.commonService.showLoader = false;
        }, 
        (error) => {
          this.alertService.error(error?.error?.error?.message);
          this.commonService.showLoader = false;
      });
    } else {
      this.commonService.showLoader = false;
      this.queryString = null;
      this.getFiles(this.activeContainer, this.currentDirectory, 1, this.records_per_page);
    }
  }
}


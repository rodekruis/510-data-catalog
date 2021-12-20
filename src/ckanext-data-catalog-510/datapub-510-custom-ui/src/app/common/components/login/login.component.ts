import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { commonService } from 'src/app/common/services/common.service';
import { AlertService } from 'src/app/common/services/alert.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  @Output() LoginResult = new EventEmitter();
  base_url: string;
  API_LIST = {
    get_databases_connections: '/api/3/action/get_db_connections',
  };
  submitted: boolean = false;
  loginForm: FormGroup;
  @Input() db_type: string;

  constructor(
    private commonService: commonService,
    private http: HttpClient,
    private alertService: AlertService
  ) {
    this.base_url = environment.base_url;
    this.loginForm = new FormGroup({
      username: new FormControl('', [Validators.required]),
      password: new FormControl('', [Validators.required])
    });
  }

  ngOnInit(): void {
  }

  onSubmit() {
    if (!this.loginForm.valid) {
      return this.commonService.validateAllFormFields(this.loginForm);
    }
    let data = {
      username: this.loginForm.get('username'),
      password: this.loginForm.get('password'),
      db_type: this.db_type
    }
    this.commonService.showLoader = true;
    this.http.post<any>(this.API_LIST.get_databases_connections, data, {})
    .subscribe((res) => {
      // sessionStorage.setItem('510_db_auth', JSON.stringify({'username': data.username, 'password': data.password}));
      this.LoginResult.emit(true);
    }, (error) => {
      this.alertService.error(error?.error?.error?.message);
      this.commonService.showLoader = false;
    });
  }

}

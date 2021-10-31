import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { InterceptorService } from './common/services/interceptor.service';
import { AlertService } from './common/services/alert.service';

import { AppComponent } from './app.component';
import { LinkComponent } from './link/link.component';
import { DatabasesComponent } from './databases/databases.component';
import { DatalakeComponent } from './datalake/datalake.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CommonCustomModule } from './common/common.module';
import { DatalakeBrowserComponent } from './datalake-browser/datalake-browser.component';

@NgModule({
  declarations: [
    AppComponent,
    LinkComponent,
    DatabasesComponent,
    DatalakeComponent,
    DatalakeBrowserComponent,
  ],
  imports: [
    BrowserModule,
    NgbModule,
    FormsModule,
    ReactiveFormsModule,
    CommonCustomModule,
    HttpClientModule,
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: InterceptorService,
      multi: true,
    },
    AlertService,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}

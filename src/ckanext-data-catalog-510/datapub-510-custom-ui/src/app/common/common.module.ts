import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { commonComponents } from './components';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LoginComponent } from './components/login/login.component';

@NgModule({
  declarations: [...commonComponents, LoginComponent],
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  exports: [FormsModule, ReactiveFormsModule, ...commonComponents],
})
export class CommonCustomModule {}

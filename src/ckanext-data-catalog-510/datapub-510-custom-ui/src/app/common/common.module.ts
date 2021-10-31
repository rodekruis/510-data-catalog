import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { commonComponents } from './components';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [...commonComponents],
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  exports: [FormsModule, ReactiveFormsModule, ...commonComponents],
})
export class CommonCustomModule {}

import { Injectable, EventEmitter } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormGroup, FormControl, FormArray } from '@angular/forms';

@Injectable({
  providedIn: 'root',
})
export class commonService {
  constructor() {}
  public _showLoader: EventEmitter<boolean> = new EventEmitter<boolean>(true);
  set showLoader(val: boolean) {
    this._showLoader.emit(val);
  }

  validateAllFormFields(form: FormGroup) {
    const keys = Object.keys(form.controls);
    keys.forEach((field: any) => {
      const control = form.get(field);
      if (control instanceof FormControl) {
        control.markAsTouched({ onlySelf: true });
        control.markAsDirty({ onlySelf: true });
        control.updateValueAndValidity();
      } else if (control instanceof FormGroup) {
        this.validateAllFormFields(control);
      } else if (control instanceof FormArray) {
        (<FormArray>control).controls.forEach((element: FormGroup | any) => {
          this.validateAllFormFields(element);
        });
      }
    });
  }
}

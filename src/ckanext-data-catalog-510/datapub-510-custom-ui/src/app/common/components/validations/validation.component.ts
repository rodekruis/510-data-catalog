import { Component, OnInit, Input } from '@angular/core';
import { FormControl } from '@angular/forms';
export const FormFieldValidators = {
  REQUIRED: 'required',
  MIN_LENGTH: 'minlength',
  MAX_LENGTH: 'maxlength',
  PATTERN: 'pattern',
  EMAIL: 'email',
  MIN: 'min',
  MAX: 'max',
};
@Component({
  selector: 'app-validator',
  templateUrl: './validation.component.html',
  styleUrls: ['./validation.component.css'],
})
export class ValidationComponent implements OnInit {
  constructor() {}

  @Input() control: FormControl | any;
  @Input() controlLabel = 'This field';
  @Input() messages: any;

  public _customErrorMessage: string;

  @Input() set customErrorMessage(value: string) {
    this._customErrorMessage = value;
  }

  get customerErrorMessage(): string {
    return this._customErrorMessage;
  }

  validationmessages: any[] = [];

  ngOnInit(): void {
    if (this._customErrorMessage != undefined) {
      this.setErrorMessages();
      this.control.statusChanges.subscribe(() => {
        this.setErrorMessages();
      });
    } else {
      this.setErrorMessages();
      this.control.statusChanges.subscribe(() => {
        this.setErrorMessages();
      });
    }
  }

  setErrorMessages() {
    if (!this.control.dirty && !this.control.touched) {
      return;
    }

    this.validationmessages = [];

    for (const propertyName in this.control.errors) {
      // FOR REQUIRED FILED VALIDATOR
      if (propertyName === FormFieldValidators.REQUIRED) {
        if (this.messages && this.messages.required) {
          this.validationmessages.push(this.messages.required);
        } else {
          this.validationmessages.push(this.controlLabel + ' is required');
        }
        // FOR MIN LENGTH FILED VALIDATOR
      } else if (propertyName === FormFieldValidators.MIN_LENGTH) {
        if (this.messages && this.messages.minlength) {
          const requiredLength = this.control.errors.minlength.requiredLength;
          let message = this.messages.minlength.replace('^^', requiredLength);
          this.validationmessages.push(message);
        } else {
          const requiredLength = this.control.errors.minlength.requiredLength;
          this.validationmessages.push(
            this.controlLabel +
              ' must be at least ' +
              requiredLength +
              ' characters long.'
          );
        }
        // FOR MAX LENGTH FILED VALIDATOR
      } else if (propertyName === FormFieldValidators.MAX_LENGTH) {
        if (this.messages && this.messages.maxlength) {
          const requiredLength = this.control.errors.maxlength.requiredLength;
          let message = this.messages.maxlength.replace('^^', requiredLength);
          this.validationmessages.push(message);
        } else {
          const requiredLength = this.control.errors.maxlength.requiredLength;
          this.validationmessages.push(
            this.controlLabel +
              ' needs to contain at most ' +
              requiredLength +
              ' characters.'
          );
        }
        // FOR PATTERN FILED VALIDATOR
      } else if (propertyName === FormFieldValidators.PATTERN) {
        if (this.messages && this.messages.pattern) {
          this.validationmessages.push(this.messages.pattern);
        } else {
          this.validationmessages.push('Please enter valid input');
        }
        // FOR EMAIL FILED VALIDATOR
      } else if (propertyName === FormFieldValidators.EMAIL) {
        if (this.messages && this.messages.email) {
          this.validationmessages.push(this.messages.email);
        } else {
          this.validationmessages.push('Please enter valid email');
        }
        // FOR MIN FILED VALIDATOR
      } else if (propertyName === FormFieldValidators.MIN) {
        if (this.messages && this.messages.min) {
          this.validationmessages.push(this.messages.min);
        } else {
          const minimum = this.control.errors.min.min;
          this.validationmessages.push(
            this.controlLabel + ' needs a minimum value of ' + minimum
          );
        }
        // FOR MAX FILED VALIDATOR
      } else if (propertyName === FormFieldValidators.MAX) {
        if (this.messages && this.messages.max) {
          this.validationmessages.push(this.messages.max);
        } else {
          const maximum = this.control.errors.max.max;
          this.validationmessages.push(
            this.controlLabel + ' needs a maximum value of ' + maximum
          );
        }
      } else if (propertyName === 'validatePhoneNumber') {
        this.validationmessages.push('Please enter valid phone no');
      }
    }
  }
}

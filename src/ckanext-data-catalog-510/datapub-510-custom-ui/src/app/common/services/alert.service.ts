import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AlertService {
  private subject = new Subject<any>();

  constructor() {}

  success(message: string) {
    this.subject.next({ type: 'success', text: message });
    this.clearMessage();
  }

  error(message: string) {
    this.subject.next({ type: 'error', text: message });
    this.clearMessage();
  }

  clearMessage() {
    let that = this;
    setTimeout(function () {
      that.subject.next({ type: '', text: '' });
    }, 2500);
  }

  getMessage(): Observable<any> {
    return this.subject.asObservable();
  }
}

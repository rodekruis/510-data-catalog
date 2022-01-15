import { Component, OnInit, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-searchbar',
  templateUrl: './searchbar.component.html',
  styleUrls: ['./searchbar.component.css']
})
export class SearchbarComponent implements OnInit {
  timeout: any = null;

  @Output() onQueryChange: EventEmitter<string> = new EventEmitter();

  constructor() { }

  ngOnInit() {}

  submitQuery(queryString: string) {
    this.onQueryChange.emit(queryString);
  }

  handleInput(event: any) {
    clearTimeout(this.timeout);
    this.timeout = setTimeout(() => {
      if(event.keyCode != 13) {
        this.submitQuery(event.target.value);
      }
    }, 500)
  }

}

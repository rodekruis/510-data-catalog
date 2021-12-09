import {
  Component,
  Input,
  OnChanges,
  Output,
  EventEmitter,
} from '@angular/core';

@Component({
  selector: 'app-pagination',
  templateUrl: './pagination-component.html',
  styleUrls: ['./pagination-component.css'],
})
export class PaginationComponent implements OnChanges {
  @Input() totalRecords = 0;
  @Input() recordsPerPage = 0;

  @Output() onPageChange: EventEmitter<number> = new EventEmitter();

  public pages: number[] = [];
  displayPages: number[] = [];
  pageRecords: number = 5;
  activePage: number;

  ngOnChanges(changes): any {
    const pageCount = this.getPageCount();
    this.pages = this.getArrayOfPage(pageCount);
    this.activePage = 1;
    this.setDisplayPage();
    this.onPageChange.emit(this.activePage);
  }

  private getPageCount(): number {
    let totalPage = 0;

    if (this.totalRecords > 0 && this.recordsPerPage > 0) {
      const pageCount = this.totalRecords / this.recordsPerPage;
      const roundedPageCount = Math.floor(pageCount);

      totalPage =
        roundedPageCount < pageCount ? roundedPageCount + 1 : roundedPageCount;
    }

    return totalPage;
  }

  private getArrayOfPage(pageCount: number): number[] {
    const pageArray = [];

    if (pageCount > 0) {
      for (let i = 1; i <= pageCount; i++) {
        pageArray.push(i);
      }
    }

    return pageArray;
  }

  private setDisplayPage(): void {
    let start_index = 0;
    let end_index = this.pages.length;
    if (this.activePage < this.pageRecords) {
      if (this.pages.length > this.pageRecords) {
        end_index = this.pageRecords + 1;
      }
    } else {
      if(this.pages.length - this.activePage < (this.pageRecords / 2) + 1) {
        start_index = this.pages.length - this.pageRecords;
        end_index = this.pages.length;
      } else {
        start_index = this.activePage - (this.pageRecords / 2);
        end_index = this.activePage + (this.pageRecords / 2) + 1;
      }
    }
    this.displayPages = this.pages.slice(start_index, end_index);
  }

  onClickPage(pageNumber: number): void {
    if (pageNumber >= 1 && pageNumber <= this.pages.length) {
      this.activePage = pageNumber;
      this.setDisplayPage();
      this.onPageChange.emit(this.activePage);
    }
  }
}

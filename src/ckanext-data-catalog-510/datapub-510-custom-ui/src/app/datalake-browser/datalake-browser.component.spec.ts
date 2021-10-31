import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatalakeBrowserComponent } from './datalake-browser.component';

describe('DatalakeBrowserComponent', () => {
  let component: DatalakeBrowserComponent;
  let fixture: ComponentFixture<DatalakeBrowserComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DatalakeBrowserComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DatalakeBrowserComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatalakeComponent } from './datalake.component';

describe('DatalakeComponent', () => {
  let component: DatalakeComponent;
  let fixture: ComponentFixture<DatalakeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DatalakeComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DatalakeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

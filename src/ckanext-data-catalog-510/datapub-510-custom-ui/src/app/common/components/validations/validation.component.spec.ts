import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ValidatorComponent } from './validation.component';

describe('ValidatorComponent', () => {
  let component: ValidatorComponent;
  let fixture: ComponentFixture<ValidatorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ValidatorComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ValidatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

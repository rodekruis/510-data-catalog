import { TestBed } from '@angular/core/testing';

import { commonService } from './common.service';

describe('commonService', () => {
  let service: commonService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(commonService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

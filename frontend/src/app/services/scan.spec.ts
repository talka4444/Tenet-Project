import { TestBed } from '@angular/core/testing';

import { Scan } from './scan.service';

describe('Scan', () => {
  let service: Scan;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Scan);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

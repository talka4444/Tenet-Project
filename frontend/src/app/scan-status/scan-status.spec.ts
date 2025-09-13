import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ScanStatus } from './scan-status';

describe('ScanStatus', () => {
  let component: ScanStatus;
  let fixture: ComponentFixture<ScanStatus>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ScanStatus]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ScanStatus);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

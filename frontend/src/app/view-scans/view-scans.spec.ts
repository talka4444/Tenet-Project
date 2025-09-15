import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewScans } from './view-scans';

describe('ViewScans', () => {
  let component: ViewScans;
  let fixture: ComponentFixture<ViewScans>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewScans]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewScans);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

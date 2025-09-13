import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateScan } from './create-scan';

describe('CreateScan', () => {
  let component: CreateScan;
  let fixture: ComponentFixture<CreateScan>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateScan]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateScan);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

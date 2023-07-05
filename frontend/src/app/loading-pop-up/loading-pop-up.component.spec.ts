import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoadingPopUpComponent } from './loading-pop-up.component';

describe('LoadingPopUpComponent', () => {
  let component: LoadingPopUpComponent;
  let fixture: ComponentFixture<LoadingPopUpComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LoadingPopUpComponent]
    });
    fixture = TestBed.createComponent(LoadingPopUpComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfoPopUpComponent } from './info-pop-up.component';

describe('InfoPopUpComponent', () => {
  let component: InfoPopUpComponent;
  let fixture: ComponentFixture<InfoPopUpComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [InfoPopUpComponent]
    });
    fixture = TestBed.createComponent(InfoPopUpComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

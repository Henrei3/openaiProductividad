import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfoOneButtonComponent } from './info-one-button.component';

describe('InfoOneButtonComponent', () => {
  let component: InfoOneButtonComponent;
  let fixture: ComponentFixture<InfoOneButtonComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [InfoOneButtonComponent]
    });
    fixture = TestBed.createComponent(InfoOneButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

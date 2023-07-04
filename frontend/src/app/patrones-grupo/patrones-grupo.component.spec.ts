import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PatronesGrupoComponent } from './patrones-grupo.component';

describe('PatronesGrupoComponent', () => {
  let component: PatronesGrupoComponent;
  let fixture: ComponentFixture<PatronesGrupoComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PatronesGrupoComponent]
    });
    fixture = TestBed.createComponent(PatronesGrupoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

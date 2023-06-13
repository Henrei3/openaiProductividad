import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CalificacionesGrupoComponent } from './calificaciones-grupo.component';

describe('CalificacionesGrupoComponent', () => {
  let component: CalificacionesGrupoComponent;
  let fixture: ComponentFixture<CalificacionesGrupoComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CalificacionesGrupoComponent]
    });
    fixture = TestBed.createComponent(CalificacionesGrupoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CalificacionesComponent } from './calificaciones/calificaciones.component';
import { HomeComponent } from './home/home.component';
import { CalificacionesGrupoComponent } from './calificaciones-grupo/calificaciones-grupo.component';
import { WorkInProgressComponent } from './work-in-progress/work-in-progress.component';

const routes: Routes = [
  {
    path:'work-in-progress',
    component:WorkInProgressComponent
  },
  {
    path:'calificaciones',
    component:CalificacionesGrupoComponent
  },
  {
    path:'calificacion',
    component: CalificacionesComponent
  },
  {
    path:"**",
    component: HomeComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule {}


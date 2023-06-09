import { NgModule } from '@angular/core';
import { RouterModule, Routes, provideRouter, withComponentInputBinding } from '@angular/router';
import { CalificacionesComponent } from './calificaciones/calificaciones.component';
import { HomeComponent } from './home/home.component';
import { CalificacionesGrupoComponent } from './calificaciones-grupo/calificaciones-grupo.component';
import { WorkInProgressComponent } from './work-in-progress/work-in-progress.component';
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { Score } from './scores/scores.model';
import { PatronesGrupoComponent } from './patrones-grupo/patrones-grupo.component';

const routes: Routes = [
  {
    path: 'patrones',
    component: PatronesGrupoComponent
  },
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
    component: CalificacionesComponent,
    
  },
  {
    path:"",
    component: HomeComponent
  },
  {
    path:"**",
    component: WorkInProgressComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes,{
    bindToComponentInputs:true, onSameUrlNavigation:'reload'
  })],
  exports: [RouterModule]
})

export class AppRoutingModule {
  
}


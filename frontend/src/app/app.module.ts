import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { CalificacionesComponent } from './calificaciones/calificaciones.component';
import { HomeComponent } from './home/home.component';
import { CalificacionesGrupoComponent } from './calificaciones-grupo/calificaciones-grupo.component';
import { WorkInProgressComponent } from './work-in-progress/work-in-progress.component';
import { DataService } from './data.service';

@NgModule({
  declarations: [
    AppComponent,
    CalificacionesComponent,
    HomeComponent,
    CalificacionesGrupoComponent,
    WorkInProgressComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule
  ],
  providers: [DataService],
  bootstrap: [AppComponent]
})
export class AppModule { }

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
import { PatronesGrupoComponent } from './patrones-grupo/patrones-grupo.component';
import {MatDialogModule} from '@angular/material/dialog'
import { LoadingPopUpComponent } from './loading-pop-up/loading-pop-up.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import 'zone.js';
import { InfoPopUpComponent } from './info-pop-up/info-pop-up.component';
import { InfoOneButtonComponent } from './info-one-button/info-one-button.component';
import { RouterModule } from '@angular/router';
@NgModule({
  declarations: [
    AppComponent,
    CalificacionesComponent,
    HomeComponent,
    CalificacionesGrupoComponent,
    WorkInProgressComponent,
    PatronesGrupoComponent,
    LoadingPopUpComponent,
    InfoPopUpComponent,
    InfoOneButtonComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    MatDialogModule,
    BrowserAnimationsModule
  ],
  providers: [DataService],
  bootstrap: [AppComponent],
  
})
export class AppModule { }

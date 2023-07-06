import { Component, Inject, OnDestroy } from '@angular/core';
import { Score } from '../scores/scores.model';
import { DataService } from '../data.service';
import { Router} from '@angular/router';
import { MAT_DIALOG_DATA, MatDialog, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import {MatButtonModule} from '@angular/material/button';
import {FormsModule} from '@angular/forms';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import { CommonModule, NgIf } from '@angular/common';
import { Subscription, map } from 'rxjs';

export interface scoreData{
  name:string;
  total:string;
  tickets:any;
  audio:string;
}
export interface totalData{
  total:string;
}

export interface ticketData{
  cedente?:string;
  cierre?:string;
  convenio?:string;
  grabacion?:string;
  identificacion?:string;
  motivo?:string;
  objecciones?:string;
  saludo?:string;
}

export interface audioData{
  audio_text:string;
}

@Component({
  selector: 'app-calificaciones',
  templateUrl: './calificaciones.component.html',
  styleUrls: ['./calificaciones.component.css']
})
export class CalificacionesComponent{
  name?: number;
  tickets?: string[] | any;
  audio ?: string;
  total ?:number;

  constructor(
    private data_service:DataService,
    private route: Router, 
    private popUpCreator:MatDialog,
    private dialogRef:MatDialogRef<CalificacionesComponent>,
    @Inject(MAT_DIALOG_DATA) public data:scoreData
    ){}
    
  return(){
    this.dialogRef.close();
  }
  showTotal(){
    this.popUpCreator.open(TotalOverviewComponent,{
      data:{total:this.total}
    })
  }
  showTickets(){
    this.popUpCreator.open(TicketOverviewComponent, {
      data:{cedente:'Test'}
    })
  }

  showAudio(){
    this.popUpCreator.open(AudioOverviewComponent, {
      data:{audio_text:this.audio}
    })
  }
}

@Component({
  selector:'total-overview-component',
  templateUrl:'total_overview.html',
  styleUrls: ['overview.components.css'],
  standalone: true,
  imports: [MatDialogModule, MatFormFieldModule, MatInputModule, FormsModule, MatButtonModule, NgIf,CommonModule],
})
export class TotalOverviewComponent {
  constructor(public dialogRef:MatDialogRef<TotalOverviewComponent>,
    @Inject(MAT_DIALOG_DATA) public data:totalData){}
}

@Component({
  selector:'ticket-overview-component',
  templateUrl:'ticket_overview.html',
  styleUrls: ['overview.components.css'],
  standalone: true,
  imports: [MatDialogModule, MatFormFieldModule, MatInputModule, FormsModule, MatButtonModule, NgIf, CommonModule],
})
export class TicketOverviewComponent{
  constructor(public dialogRef:MatDialogRef<TicketOverviewComponent>,
    @Inject(MAT_DIALOG_DATA) public data:ticketData){}
}

@Component({
  selector:'audio-overview-component',
  templateUrl:'audio_overview.html',
  styleUrls: ['overview.components.css'],
  standalone: true,
  imports: [MatDialogModule, MatFormFieldModule, MatInputModule, FormsModule, MatButtonModule,NgIf, CommonModule],
})
export class AudioOverviewComponent{
  constructor(public dialogRef:MatDialogRef<AudioOverviewComponent>,
    @Inject(MAT_DIALOG_DATA) public data:audioData){}
}

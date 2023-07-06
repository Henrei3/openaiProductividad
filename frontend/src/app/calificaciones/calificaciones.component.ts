import { Component, Inject, OnDestroy } from '@angular/core';
import { Score } from '../scores/scores.model';
import { DataService } from '../data.service';
import { Router} from '@angular/router';
import { MAT_DIALOG_DATA, MatDialog, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import {MatButtonModule} from '@angular/material/button';
import {FormsModule} from '@angular/forms';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import { CommonModule, NgClass, NgFor, NgForOf, NgIf } from '@angular/common';
import { Subscription, map } from 'rxjs';
import { NO_ERRORS_SCHEMA } from '@angular/compiler';

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
  tickets: Array<string>
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
      data:{total:this.data.total},
      disableClose:false
    })
  }
  showTickets(){
    
    var ticket_list = Object.keys(this.data.tickets)
    var data_content = new Array<string>;
    for (let i = 0; i < ticket_list.length; i++){
      let actual_ticket = ticket_list[i];
      data_content.push(actual_ticket + ' :' + this.data.tickets[actual_ticket])
    }
    
    this.popUpCreator.open(TicketOverviewComponent, {
      data:{tickets: data_content},
      disableClose: false
    })
  }

  showAudio(){
    this.popUpCreator.open(AudioOverviewComponent, {
      data:{audio_text: this.data.audio},
      disableClose:false
    })
  }
}

@Component({
  selector:'total-overview-component',
  templateUrl:'total_overview.html',
  styleUrls: ['overview.components.css'],
  standalone: true,
  imports: [MatDialogModule, MatFormFieldModule, MatInputModule, FormsModule, MatButtonModule, NgFor,CommonModule],
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
  imports: [MatDialogModule, MatFormFieldModule, MatInputModule, 
    FormsModule, MatButtonModule, CommonModule, NgForOf,NgFor,NgClass],
    
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
  imports: [MatDialogModule, MatFormFieldModule, MatInputModule, FormsModule, MatButtonModule,NgFor, CommonModule],
})
export class AudioOverviewComponent{
  constructor(public dialogRef:MatDialogRef<AudioOverviewComponent>,
    @Inject(MAT_DIALOG_DATA) public data:audioData){}
}

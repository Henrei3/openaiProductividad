import { Component, Input } from '@angular/core';
import { Score } from '../scores/scores.model';
import { DataService } from '../data.service';
import { Router} from '@angular/router';

@Component({
  selector: 'app-calificaciones',
  templateUrl: './calificaciones.component.html',
  styleUrls: ['./calificaciones.component.css']
})
export class CalificacionesComponent {
  total ?:number
  tickets ?: JSON
  audio ?: String

  score ?:Score;
  
  constructor(private data_service:DataService, private route: Router){
    data_service.data$.subscribe(x => this.score = x)
    console.log(this.score)
  }
  
  return(){
    this.route.navigate(['/calificaciones'])
  }
  showTotal(){
    this.tickets = undefined
    this.audio = undefined
    this.total = this.score!.total
  }
  showTickets(){
    this.tickets = this.score!.ticket_score
    this.total = undefined
    this.audio = undefined
  }

  showAudio(){
    this.audio=this.score?.audio_text
    this.tickets = undefined
    this.total = undefined
  }
}


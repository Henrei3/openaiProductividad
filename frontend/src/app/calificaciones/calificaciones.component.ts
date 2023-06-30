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
  s_id?: number
  tickets?: string[] | any
  audio ?: String

  total ?:number;
  
  constructor(private data_service:DataService, private route: Router){
    data_service.data$.subscribe(sentData => {
      this.s_id = sentData.s_id
      this.total = sentData.score["total"];
      this.tickets = sentData.score["ticket_score"]
    })
  }
  
  return(){
    this.route.navigate(['/calificaciones'])
  }
  showTotal(){
    
    console.log(this.total)

  }
  showTickets(){
    console.log(this.tickets)
  }

  showAudio(){
    console.log(this.audio)
  }
}

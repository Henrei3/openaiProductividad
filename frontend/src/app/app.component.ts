import { Component,Input} from '@angular/core';
import { Subscription } from 'rxjs';
import { Score } from './scores/scores.model';
import { BackendService } from './backend-service.service';
import { DataService } from './data.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'frontend';
  
  dataPassed :any;
  subsciption?: Subscription;
  
  constructor(private data_service:DataService){
    this.subsciption = this.data_service.data$.subscribe(scores => {
    this.data_service.sendData(scores);
    this.dataPassed = scores;  
    });
  
  }
}

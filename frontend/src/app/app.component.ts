import { Component,OnInit,OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { RecordingsApiService } from './recordings/recordings-api.service';
import { Recordings } from './recordings/recordings.model';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit,OnDestroy{
  title = 'frontend';

  recordListSubs!: Subscription;
  recordLists!: Recordings[]

constructor(private recordings : RecordingsApiService) {
  
}

  ngOnInit(): void {
    const obsArgument = {
      next: (solution: Recordings[]) => {
        this.recordLists = solution
        console.log(solution)
      }, 
      error: (err : Error) => console.error('Observer got an error : ' + err) 
    }
    
    this.recordListSubs = this.recordings
    .get_Records()  
    .subscribe( obsArgument );
  }
  ngOnDestroy(): void {
      this.recordListSubs.unsubscribe()
  }
}

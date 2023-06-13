import { Component,OnInit,OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { Gestion } from './recordings/recordings.model';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit,OnDestroy{
  title = 'frontend';

  recordListSubs!: Subscription;
  recordLists!: Gestion[]



  ngOnInit(): void {
    const obsArgument = {
      next: (solution: Gestion[]) => {
        this.recordLists = solution
        console.log(solution)
        console.log("test")
      },
      error: (err : Error) => console.error('Observer got an error : ' + err)
    }

  }
  ngOnDestroy(): void {
      this.recordListSubs.unsubscribe()
  }
}

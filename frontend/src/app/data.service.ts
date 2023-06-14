import { Injectable } from '@angular/core';
import {Observable} from 'rxjs'
import {BehaviorSubject, Subject} from 'rxjs'
import { Score } from './scores/scores.model';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  private data:Subject<any> = new BehaviorSubject<any>([]);

  sendData(score:Score | Score[]){
    this.data.next(score)
  }

  get data$():Observable<any>{
    return this.data.asObservable();
  }
}

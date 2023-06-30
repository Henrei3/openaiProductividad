import { Injectable } from '@angular/core';
import axios from 'axios'
@Injectable({
  providedIn: 'root'
})
export class BackendService {

  constructor() { }

  executeScoreCalculations(y:string, m:string, d:string){
    let date = '{"year":"'+y+'","month":"'+m+'","day":"'+d+'"}'

    return axios.post("http://127.0.0.1:5000/records", date)
  }
}

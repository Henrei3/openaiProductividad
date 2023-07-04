import { Injectable } from '@angular/core';
import axios from 'axios'
@Injectable({
  providedIn: 'root'
})
export class BackendService {

  constructor() { }

  executeScoreCalculations(y:string, m:string, d:string){
    let date = this.generateJSON(y,m,d)

    return axios.post("http://127.0.0.1:5000/records", date)
  }
  executePatternPriceSearch(y:string, m:string, d:string){
    let date = this.generateJSON(y,m,d);

    return axios.post("http://127.0.0.1:5000/patternPrice", date)
  }

  generateJSON(y:string, m:string, d:string){
      return '{"year":"'+y+'","month":"'+m+'","day":"'+d+'"}'
  }
}

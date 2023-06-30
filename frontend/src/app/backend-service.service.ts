import { Injectable } from '@angular/core';
import axios from 'axios'
@Injectable({
  providedIn: 'root'
})
export class BackendService {

  constructor() { }

  executeScoreCalculations(){
    return axios.post("http://127.0.0.1:5000/records",{year:'value1',month:'value2',day:'value3'})
  }
}


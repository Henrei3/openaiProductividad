import { Injectable } from '@angular/core';
import axios from 'axios'
@Injectable({
  providedIn: 'root'
})
export class BackendService {

  constructor() { }

  //Quality Assurance Axios Calls
  
  executeScorePriceCalculations(y:string, m:string, d:string){
    let date = this.generateJSON(y,m,d)

    return axios.post("http://127.0.0.1:5000/records", date)
  }

  executeAudioTransformationScoreCalculation(){
    return axios.get("http:://127.0.0.1:5000/records")
  }

  fetchScores(){
    return axios.get("http:://127.0.0.1:5000/scoreFetch")
  }
  // Pattern Search / Gestiones de pagos Axios Calls
  executePatternPriceSearch(y:string, m:string, d:string){
    let date = this.generateJSON(y,m,d);

    return axios.post("http://127.0.0.1:5000/patternPrice", date)
  }
  executeAudioTransformationEmbeddingsCalculation(){
    return axios.get("http://127.0.0.1:5000/audioTranformationEmbeddingsCalculation")
  }
  executeEmbeddingGeneration(){
    return axios.get("http://127.0.0.1:5000/embeddingsGeneration")
  }

  generateJSON(y:string, m:string, d:string){
      return '{"year":"'+y+'","month":"'+m+'","day":"'+d+'"}'
  }
}

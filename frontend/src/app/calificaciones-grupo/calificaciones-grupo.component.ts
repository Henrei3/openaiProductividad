import { Component, OnInit } from '@angular/core';
import axios from 'axios'
import { BackendService} from '../backend-service.service';
import { Router } from '@angular/router';
import { AbstractFormGroupDirective } from '@angular/forms';
import { AppComponent } from '../app.component';
import { DataService } from '../data.service';
import { Score } from '../scores/scores.model';


@Component({
  selector: 'app-calificaciones-grupo',
  templateUrl: './calificaciones-grupo.component.html',
  styleUrls: ['./calificaciones-grupo.component.css']
})

export class CalificacionesGrupoComponent implements OnInit{

  scores: Score[]= [];

  constructor(private scoreCalculs : BackendService, private dataService: DataService, private route: Router){}

  ngOnInit(){
    let dateSelector = document.getElementsByTagName("input")
 
    let values:number[] = [4,2,2];

    for (let i = 0; i < dateSelector.length; i++){
   
      dateSelector[i].addEventListener("keyup", (e)=>{ 
      if(values[i] <= dateSelector[i].value.length && e.key !="ArrowRight" ){
        if (i != dateSelector.length-1 && e.key!="ArrowLeft") dateSelector[i+1].select(); 
      }
      if(dateSelector[i].value.length <=  0 && e.key == "Backspace"){
        if(i -1 >= 0){dateSelector[i-1].select()}
      }
      if(i == dateSelector.length-1 && e.key=="Enter"){
        console.log("calculating...")
        let y:string = dateSelector[0].value
        let m:string = dateSelector[1].value
        let d:string = dateSelector[2].value
        this.getScores(y,m,d)
      }
      })
    }
  }


  getScores(y: string, m:string, d:string){
    this.scoreCalculs.executeScoreCalculations(y, m, d)
    .then((response)=>{    

      let variable = Object.keys(response.data)


      for (let i=0; i < variable.length; i++){
        let s_id = variable[i]  
        
        let score_json = response.data[s_id]
        
        let score = new Score(s_id, score_json)
        
        console.log(score)

        this.scores.push(score)
      }  
    })
    .catch((err)=>{
      console.error(err)
    })
  }

  showScore(s_id:any ){
    for(let i=0; i<this.scores.length; i++){
      
      if(this.scores[i].s_id == s_id) {
        
        this.dataService.sendData(this.scores[i])}
    }
    this.route.navigate(['/calificacion'])
  }
}

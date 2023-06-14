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
      if(i == dateSelector.length-1 && e.key=="Enter"){
        console.log("calculating...")
        this.getScores()
      }
      })
    }
  }
  
  showScore(name:any ){
    for(let i=0; i<this.scores.length; i++){
      if(this.scores[i].name == name) this.dataService.sendData(this.scores[i])
    }
    this.route.navigate(['/calificacion'])
  }

  getScores(){
    this.scoreCalculs.executeScoreCalculations()
    .then((response)=>{    
      let variable = Object.keys(response.data)
    
      for (let i=0; i < variable.length; i++){
        let name = variable[i]  
        
        let total = response.data[name][1]["total"]
        
        let ticket_score = response.data[name][1]["ticket_score"]
        
        let audio_text = response.data[name][0]["text"]
        
        let score = new Score(name,total,ticket_score,audio_text)
        
        this.scores.push(score)
      }
      
    }

    ).catch((err)=>{
      console.error(err)
    } 
    )
  }
}

 

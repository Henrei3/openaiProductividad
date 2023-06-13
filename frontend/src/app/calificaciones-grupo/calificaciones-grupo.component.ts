import { Component, OnInit } from '@angular/core';
import axios from 'axios'
import { BackendService} from '../backend-service.service';


@Component({
  selector: 'app-calificaciones-grupo',
  templateUrl: './calificaciones-grupo.component.html',
  styleUrls: ['./calificaciones-grupo.component.css']
})
export class CalificacionesGrupoComponent implements OnInit{
  constructor(private scoreCalculs : BackendService){}

  getScores(){
    this.scoreCalculs.executeScoreCalculations()
    .then((response)=>{
      console.log(response)
      console.log(response.data)    
      let variable = Object.keys(response.data)
      console.log(response.data[variable[0]])
    }
    ).catch(()=>{
      console.error()
    } 
    )
  }
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
        console.log("done")
      }
      })
    }
  }
}

 

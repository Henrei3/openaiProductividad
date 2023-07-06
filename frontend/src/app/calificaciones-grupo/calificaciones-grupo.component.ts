import { Component, OnInit, OnChanges, DoCheck } from '@angular/core';
import axios from 'axios'
import { BackendService} from '../backend-service.service';
import { Router } from '@angular/router';
import { AbstractFormGroupDirective } from '@angular/forms';
import { AppComponent } from '../app.component';
import { DataService } from '../data.service';
import { Score } from '../scores/scores.model';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { LoadingPopUpComponent } from '../loading-pop-up/loading-pop-up.component';
import { InfoPopUpComponent } from '../info-pop-up/info-pop-up.component';
import { InfoOneButtonComponent } from '../info-one-button/info-one-button.component';
import { CalificacionesComponent } from '../calificaciones/calificaciones.component';
import { data } from 'jquery';

@Component({
  selector: 'app-calificaciones-grupo',
  templateUrl: './calificaciones-grupo.component.html',
  styleUrls: ['./calificaciones-grupo.component.css']
})

export class CalificacionesGrupoComponent implements OnInit{

  scores: Score[]= [];

  constructor(private scoreCalculs : BackendService, private dataService: DataService, private route: Router, private popUpCreator: MatDialog){}

  ngOnInit(){
    let dateSelector = document.getElementsByTagName("input")

    let values:number[] = [4,2,2];

    for (let i = 0; i < dateSelector.length; i++){
   
      dateSelector[i].addEventListener("keyup", (e)=>{ 
      console.log("Date Selector Value : "+dateSelector[i].value)
      if(values[i] <= dateSelector[i].value.length && e.key != "ArrowRight" ){
        if (i != dateSelector.length-1 && e.key!="ArrowLeft") dateSelector[i+1].select(); 
      }
      if(dateSelector[i].value.length <=  0 && e.key == "Backspace"){
        if(i -1 >= 0){dateSelector[i-1].select()}
      }
      if(i == dateSelector.length-1 && e.key=="Enter"){
        console.log("calculating...");
        let y:string = dateSelector[0].value;
        let m:string = dateSelector[1].value;
        let d:string = dateSelector[2].value;
        for (let i = 0; i < dateSelector.length;i++){
          dateSelector[i].value = '';
        }
        this.getScoresPrice(y,m,d);
      }
      })
    }
  }

  getScoresPrice(y:string, m:string, d:string){
    this.popUpCreator.open(LoadingPopUpComponent)
    this.scoreCalculs.executeScorePriceCalculations(y,m,d).then((response)=>{
      this.popUpCreator.closeAll()
      let audio_score_response = response.data
      if(audio_score_response[1])
      {const dialogRef = this.popUpCreator.open(InfoPopUpComponent,
        {data:{message: audio_score_response[0], ok_button: 'Transformar', no_button: 'Cancel'}})
        dialogRef.afterClosed().subscribe((ok_button_text)=>{
          if (ok_button_text){
            this.calculateScores()
          }
        })
      }
      else{
          this.popUpCreator.open(InfoOneButtonComponent, {
            data:{ message:audio_score_response[0], button_text:'Ok'}
          })
      }
    }).catch((error_message)=>{
      this.popUpCreator.closeAll()
      this.popUpCreator.open(InfoOneButtonComponent, {data:{
        message:error_message, button_text:'Ok'
      }})
    })
  }

  calculateScores(){
    this.popUpCreator.open(LoadingPopUpComponent)
    this.scoreCalculs.executeAudioTransformationScoreCalculation().then((response)=>{
      this.popUpCreator.closeAll()
      let audio_tranformation_score_calculation_response = response.data
      const dialogRef = this.popUpCreator.open(InfoPopUpComponent, {
        data:{message: audio_tranformation_score_calculation_response, ok_button: 'Ver', no_button:'Cerrar'}
      })
      dialogRef.afterClosed().subscribe((ok_button_text)=>{
        if (ok_button_text){
          this.fetchScores()
        }
      })
    }).catch((error_message)=>{
      this.popUpCreator.closeAll()
      this.popUpCreator.open(InfoOneButtonComponent, {data:{
        message:error_message, button_text:'Ok'
      }})
    })
  }

  fetchScores(){
    this.scoreCalculs.fetchScores()
    .then((response)=>{    
      let score_fetch = response.data
      let scores = score_fetch[0]
      console.log(scores)
      
      if(score_fetch[1]){
      let variable = Object.keys(scores)
      
      for (let i=0; i < variable.length; i++){
        let name: string = variable[i]  
        
        let recording_info:Array<string> = scores[name]
        
        let score = new Score(name, recording_info[0],recording_info[1])
        
        console.log(score)

        this.scores.push(score)}
      }
      else{
        this.popUpCreator.open(InfoOneButtonComponent, {
          data:{message:score_fetch[0], button_text:'Ok'}
        })
      }
    })
    .catch((error_message)=>{
      this.popUpCreator.closeAll()
      this.popUpCreator.open(InfoOneButtonComponent, {data:{
        message:error_message, button_text:'Ok'
      }})
    })
  }

  showScore(name:string | undefined){
    for(let i=0; i<this.scores.length; i++){
      
      if(this.scores[i].name == name) {
        
        this.popUpCreator.open(CalificacionesComponent, {data:{
          name:''
        }})
      
      }
    }
    
  }

}

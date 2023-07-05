import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { BackendService } from '../backend-service.service';
import { Data } from '@angular/router';
import {MatDialog, MatDialogConfig} from '@angular/material/dialog'
import { LoadingPopUpComponent } from '../loading-pop-up/loading-pop-up.component';
import { InfoPopUpComponent } from '../info-pop-up/info-pop-up.component';

@Component({
  selector: 'app-patrones-grupo',
  templateUrl: './patrones-grupo.component.html',
  styleUrls: ['./patrones-grupo.component.css']
})
export class PatronesGrupoComponent implements OnInit{
  
  public message?: string;

  popUp_button_message:any = {};

  dialogConfig : MatDialogConfig = {
    panelClass:'makeItMiddle'
  };

  constructor(private patternSearch:BackendService, private dataTransfer:DataService, private popUpCreator:MatDialog){
    this.dialogConfig.disableClose = true
  }

  ngOnInit(): void {
    
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
        this.getPatternPrice(y,m,d)
      }
      })
    }
    let okButton = document.getElementById('ok')
      if(okButton){
        okButton.addEventListener('click', ()=>{
          if(okButton?.innerHTML === "Transformar")
            this.getEmbeddingPriceCalculateAudios()
          if(okButton?.innerHTML === "Generar")
            this.calculateEmbeddings()
        })
      }
  }
  
  appear(id:string, class_to_add:string){
    let popup = document.getElementById(id);
    if(popup){
      popup.classList.add(class_to_add)  
    }
  }
  
  hide(id:string, class_to_remove:string){
    let popup = document.getElementById(id);
    if(popup){
      popup.classList.remove(class_to_remove)  
      this.message = undefined
    }
  }

  show_result(hide_id:string, hide_class:string, message:string, button_yes_message:string, appear_id:string, appear_class:string){
    this.message = message
    this.popUp_button_message['si'] = button_yes_message
    this.appear(appear_id, appear_class)
  }

  getPatternPrice(y:string, m:string, d:string){
    this.popUpCreator.open(LoadingPopUpComponent, this.dialogConfig)
    this.popUp_button_message['no'] = 'Cancelar'
    this.patternSearch.executePatternPriceSearch(y,m,d).then(
      (response)=>{
        this.popUpCreator.closeAll()
        let audio_calculation_response = response.data
        const infoPopUpRef = this.popUpCreator.open(InfoPopUpComponent, {
          data:{message: audio_calculation_response, ok_button: 'Transformar', no_button:'Cancel'}
        })
        infoPopUpRef.afterClosed().subscribe(
          (ok_button_text) => {
            if (ok_button_text == 'Transformar'){
              this.getEmbeddingPriceCalculateAudios()
            }
          }
        )
      }
    ).catch(
      (error_message)=> {
        this.popUpCreator.closeAll()
        this.popUpCreator.open(InfoPopUpComponent, {
          data:{message: error_message, ok_button: 'Ok', no_button:'Cancel'}
        })
      })
  }

  getEmbeddingPriceCalculateAudios(){
    this.popUpCreator.open(LoadingPopUpComponent, this.dialogConfig)
    this.patternSearch.executeAudioTransformationEmbeddingsCalculation().then(
      (response)=>{
        this.popUpCreator.closeAll()
        let embedding_response = response.data
        const inforPopUpRef = this.popUpCreator.open(InfoPopUpComponent, {
          data:{message: embedding_response, ok_button: 'Generate', no_button:'Cancel'}
        })
        
        inforPopUpRef.afterClosed().subscribe((ok_button_text)=>{
          if (ok_button_text == 'Generate'){
            this.calculateEmbeddings()
          }
        })

      }).catch((error_messsage)=>{
        this.popUpCreator.closeAll()
        this.popUpCreator.open(InfoPopUpComponent, {
          data:{message: error_messsage, ok_button: 'Ok', no_button:'Cancel'}
        })
      })
  }
  
  calculateEmbeddings(){
    this.popUpCreator.open(LoadingPopUpComponent, this.dialogConfig)
    this.patternSearch.executeEmbeddingGeneration().then((response)=>{
      var embedding_generation_response = response.data
      this.popUpCreator.closeAll()
      const inforPopUpRef = this.popUpCreator.open(InfoPopUpComponent, {
        data:{message: embedding_generation_response, ok_button: 'Comparar Audios', no_button:'Cancel'}
      })
      inforPopUpRef.afterClosed().subscribe((ok_button_text)=>{
        if (ok_button_text){
          console.log("work In progress ...")
        }
      })
    }).catch((error_message)=>{
      this.popUpCreator.closeAll()
      this.popUpCreator.open(InfoPopUpComponent, {
        data:{message: error_message, ok_button: 'Ok', no_button:'Cancel'}
      })
    })
  }

}

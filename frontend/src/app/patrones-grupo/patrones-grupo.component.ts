import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { BackendService } from '../backend-service.service';
import { Data } from '@angular/router';

@Component({
  selector: 'app-patrones-grupo',
  templateUrl: './patrones-grupo.component.html',
  styleUrls: ['./patrones-grupo.component.css']
})
export class PatronesGrupoComponent implements OnInit{
  
  public message?: string;

  popUp_button_message:any = {};

  constructor(private patternSearch:BackendService, private dataTransfer:DataService){}

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
    this.hide(hide_id, hide_class)
    this.message = message
    this.popUp_button_message['si'] = button_yes_message
    this.appear(appear_id, appear_class)
  }

  getPatternPrice(y:string, m:string, d:string){
    this.appear('loading', 'loading');
    this.popUp_button_message['no'] = 'Cancelar'
    this.patternSearch.executePatternPriceSearch(y,m,d).then(
      (response)=>{
        
        let audio_calculation_response = response.data
        this.show_result('loading', 'loading', audio_calculation_response, 'Transformar', 'popUp', 'poppedUp') 
        
      }
    ).catch(
      (error_message)=> {

        this.show_result('loading', 'loading', error_message, 'Ok', 'popUp', 'poppedUp')
      
      })
  }

  getEmbeddingPriceCalculateAudios(){
    this.appear('loading', 'loading')
    this.patternSearch.executeAudioTransformationEmbeddingsCalculation().then(
      (response)=>{

        let embedding_response = response.data
        this.show_result('loading', 'loading',embedding_response, 'Generar', 'popUp', 'poppedUp')

      }).catch((error_messsage)=>{

        this.show_result('loading', 'loading', error_messsage, 'Ok', 'popUp', 'poppedUp')
     
      })
  }
  
  calculateEmbeddings(){
    this.appear('loading', 'loading')
    this.patternSearch.executeEmbeddingGeneration().then((response)=>{
      var embedding_generation_response = response.data
      this.show_result('loading','loading',embedding_generation_response,'Comparar un audio', 'popUp', 'poppedUp')
    }).catch((error_message)=>{

      this.show_result('loading', 'loading', error_message, 'Ok', 'popUp', 'poppedUp')

    })
  }
}

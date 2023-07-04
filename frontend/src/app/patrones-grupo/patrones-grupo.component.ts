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
  }
  getPatternPrice(y:string, m:string, d:string){
    this.appear('loading', 'loading');
    this.popUp_button_message['no'] = 'Cancelar'
    this.patternSearch.executePatternPriceSearch(y,m,d).then(
      (response)=>{
        let variable = response.data
        console.log(variable)
        this.message = variable 
        this.hide('loading', 'loading')
        this.popUp_button_message['si'] = 'Calcular Audios'
        
        this.appear('popUp', 'poppedUp')
      }
    ).catch(
      (error_message)=> {
        this.hide('loading', 'loading')
        this.message = 'Hubo un error calculando los patrones: ' + '\n'+ error_message
        this.popUp_button_message['si'] = 'Ok' 
        this.appear('popUp','poppedUp')
      })
  }
  appear(id:string, class_to_add:string){
    let popup = document.getElementById(id);
    if(popup){
      popup.classList.add(class_to_add)  
      let okButton = document.getElementById('ok')
      if(okButton){
        okButton.onclick = function(){
          if(okButton?.innerHTML === 'Calcular Audios' ){
            alert('Los audios se estan calculando')
          } 
        }
      }
    }
  }
  hide(id:string, class_to_remove:string){
    let popup = document.getElementById(id);
    if(popup){
      popup.classList.remove(class_to_remove)  
      this.message = undefined
    }
  }
}

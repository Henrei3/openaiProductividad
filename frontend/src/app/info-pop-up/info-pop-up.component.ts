import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

export interface popUpData{
  message:string;
  ok_button:string;
  no_button:string;
}


@Component({
  selector: 'app-info-pop-up',
  templateUrl: './info-pop-up.component.html',
  styleUrls: ['./info-pop-up.component.css']
})
export class InfoPopUpComponent {
 constructor(private dialogRef:MatDialogRef<InfoPopUpComponent>,
  @Inject(MAT_DIALOG_DATA) public data: popUpData){}

  clickNoButton(){
    this.dialogRef.close()
  }
}
  
  

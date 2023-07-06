import { Component, Inject } from '@angular/core';
import { inject } from '@angular/core/testing';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

export interface OneButtonData{
  message:string;
  button_text:string;
}

@Component({
  selector: 'app-info-one-button',
  templateUrl: './info-one-button.component.html',
  styleUrls: ['./info-one-button.component.css']
})
export class InfoOneButtonComponent {
  constructor(private dialogRef: MatDialogRef<InfoOneButtonComponent>,
    @Inject(MAT_DIALOG_DATA) public data: OneButtonData){}


    clickButton(){
      this.dialogRef.close();
    }
}

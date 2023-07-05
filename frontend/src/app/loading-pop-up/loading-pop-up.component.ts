import { Component } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog'

@Component({
  selector: 'app-loading-pop-up',
  templateUrl: './loading-pop-up.component.html',
  styleUrls: ['./loading-pop-up.component.css']
})
export class LoadingPopUpComponent {
  constructor(public dialogRef:MatDialogRef<LoadingPopUpComponent>){}

  close(): void {
    this.dialogRef.close()
  }
}

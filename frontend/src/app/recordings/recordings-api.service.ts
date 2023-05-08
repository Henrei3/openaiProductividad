import { API_URL } from "../env";

import { Injectable } from "@angular/core";

import {HttpClient, HttpErrorResponse} from '@angular/common/http';

import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';


import { Recordings } from "./recordings.model";
 
@Injectable()
export class RecordingsApiService{
    constructor(private http:HttpClient){}

    private _handleError(error: HttpErrorResponse) {
        if (error.status === 0) {
          // A client-side or network error occurred. Handle it accordingly.
          console.error('An error occurred:', error.error);
        } else {
          // The backend returned an unsuccessful response code.
          // The response body may contain clues as to what went wrong.
          console.error(
            `Backend returned code ${error.status}, body was: `, error.error);
        }
        // Return an observable with a user-facing error message.
        return throwError(() => new Error('Something bad happened; please try again later.'));
      }

    get_Records(): Observable<Recordings[]> {
        
        return this.http
      .get<Recordings[]>(`${API_URL}/records`)
      .pipe(
        catchError(this._handleError)
      );
    }

}



// import { Component } from '@angular/core';
// import { HttpClient } from '@angular/common/http';
// import { Router } from '@angular/router';
// import { HttpClientModule } from '@angular/common/http';

// @Component({
//   selector: 'app-upload',
//   templateUrl: './upload.component.html',
//   styleUrls: ['./upload.component.scss']
// })
// export class UploadComponent {
//   files: any;
  
  

  

//   constructor(private router: Router) {}
  
//     redirect() {
        
//         this.router.navigate(['/dashboard']);
//       }
//       onSubmit() {
//         const formData = new FormData();
//         formData.append('file', this.files[0]);
    
//         this.http.post<any>('http://localhost:5000/upload', formData).subscribe(
//           (response: any) => {
//             console.log(response);
//             this.response = response;
//           },
//           (error) => {
//             console.log(error);
//           }
//         );
//       }

      
//   }

  import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})
export class UploadComponent {
  title= 'Upload';

  files: File[] = [];

  response : any;
  constructor(private http: HttpClient) { }

  onSelect(event: { addedFiles: any; }) {
    console.log(event);
    this.files.push(...event.addedFiles);
  }

  onRemove(event: File) {
    console.log(event);
    this.files.splice(this.files.indexOf(event), 1);
  }

  onSubmit() {
    const formData = new FormData();
    formData.append('file', this.files[0]);

    this.http.post<any>('http://localhost:5000/upload', formData).subscribe(
      (response) => {
        console.log(response);
        this.response = response;
      },
      (error) => {
        console.log(error);
      }
    );
  }
  formData = {
    year: '',
    month: '',
    pid: ''
  };
  onPredict() {
    this.http.post<any[]>('http://localhost:5000/form', this.formData).subscribe(
      (response) => { this.response = response;},
      (error) => { console.log(error); }
    );
  }
}



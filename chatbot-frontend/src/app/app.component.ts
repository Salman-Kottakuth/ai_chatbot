import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true, // Indicates this is a standalone component
  imports: [RouterOutlet, HttpClientModule],
  // templateUrl: './app.component.html',
  template: `
    <router-outlet></router-outlet>
  `,
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'chatbot-frontend';
}

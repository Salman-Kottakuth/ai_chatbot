import { Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { ChatbotComponent } from './chatbot/chatbot.component'; // Adjust the import path as needed

export const routes: Routes = [
  { path: '', component: AppComponent },  // Main app component
  { path: 'full-chatbot', component: ChatbotComponent },  // Full-page chatbot route
];

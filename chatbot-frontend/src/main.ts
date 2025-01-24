import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

import { provideHttpClient } from '@angular/common/http';
import { ChatbotComponent } from './app/chatbot/chatbot.component';

bootstrapApplication(ChatbotComponent, {
  providers: [provideHttpClient()], // Ensure the HTTP client is provided
});
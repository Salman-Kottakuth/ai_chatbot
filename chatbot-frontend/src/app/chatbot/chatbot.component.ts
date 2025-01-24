import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common'; // Import CommonModule
import { FormsModule } from '@angular/forms';   // Import FormsModule

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule], // Add CommonModule and FormsModule here
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css'],
})
export class ChatbotComponent {
  messages: { sender: string; text: string }[] = [];
  userInput: string = '';

  constructor(private http: HttpClient) {}

  sendMessage() {
    if (!this.userInput.trim()) return;

    const userMessage = this.userInput;
    this.messages.push({ sender: 'user', text: userMessage });
    this.userInput = '';

    this.http
      .post<{ response: string }>('http://your-backend-api/chat', {
        message: userMessage,
      })
      .subscribe((response) => {
        this.messages.push({ sender: 'bot', text: response.response });
      });
  }
}

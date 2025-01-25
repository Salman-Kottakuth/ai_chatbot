import { Component } from '@angular/core';
import { NgIf, NgFor, NgClass } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [NgIf, NgFor, NgClass, FormsModule],
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css'],
})
export class ChatbotComponent {
  chatVisible: boolean = false; // Toggles the chat window visibility
  userInput: string = ''; // Holds the current user input
  messages: { text: string; sender: 'user' | 'bot' }[] = []; // Holds chat messages

  private backendUrl = 'http://localhost:8000/getAnswer'; // Backend API endpoint

  constructor(private http: HttpClient) {}

  // Toggles the chat visibility
  toggleChat(): void {
    this.chatVisible = !this.chatVisible;
  }

  // Sends a message to the backend
  sendMessage(): void {
    if (this.userInput.trim() === '') {
      return; // Ignore empty input
    }

    // Add the user's message to the chat
    this.messages.push({ text: this.userInput, sender: 'user' });

    // Make a POST request to the backend
    this.http.post(this.backendUrl, { question: this.userInput }).subscribe(
      (response: any) => {
        // Parse the bot's response and add it to the chat
        if (response && response[0]?.answer) {
          this.messages.push({ text: response[0].answer, sender: 'bot' });
        } else {
          this.messages.push({ text: 'No response from the bot.', sender: 'bot' });
        }
      },
      (error) => {
        console.error('Error communicating with the backend:', error);
        this.messages.push({ text: 'Error: Could not connect to the server.', sender: 'bot' });
      }
    );

    // Clear the input field
    this.userInput = '';
  }
}
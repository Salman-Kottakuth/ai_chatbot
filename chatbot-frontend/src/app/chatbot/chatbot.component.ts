import { Component } from '@angular/core';
import { NgIf, NgFor, NgClass } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [NgIf, NgFor, NgClass, FormsModule],
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css'],
})
export class ChatbotComponent {
  chatVisible = false;
  userInput = '';
  messages: { text: string; sender: 'user' | 'bot' }[] = [];

  toggleChat() {
    this.chatVisible = !this.chatVisible;
  }

  sendMessage() {
    if (this.userInput.trim()) {
      this.messages.push({ text: this.userInput, sender: 'user' });
      this.userInput = '';

      // Mock response
      this.messages.push({ text: 'This is a response from the bot.', sender: 'bot' });
    }
  }
}


from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from src.chatbot.chatbot_backend import ChatBot 
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Frontend URL (Angular app)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define a Pydantic model for the request payload
class UserMessageRequest(BaseModel):
    question: str  # user's message input



# Serve static files 
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates for rendering html
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_chat_ui(request: Request):
    """
    Returns the HTML page that contains the chat interface.
    """
    # Render the HTML page using Jinja2
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/getAnswer")
async def chat_endpoint(request: UserMessageRequest):
    """
    Handles the user message, processes it through the chatbot, and returns the response.

    Args:
        request (UserMessageRequest): Contains the user's message input.

    Returns:
        JSONResponse: The chatbot's response to the user's message.
    """
    try:
        # Get the message from the request
        user_message = request.question  

        # Pass the user message to ChatBot 
        _, chatbot_response = ChatBot.respond(user_message)

        
        # Prepare the response as an array of JSON objects
        response_data = [{
            "answer": chatbot_response,
            "serviceId": 2, 
            "type": "text" 
        }]

        # Return the bot's response as JSON array
        return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")
    


# If run directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)



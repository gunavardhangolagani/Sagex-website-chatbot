# Sagex Website Chatbot

Sagex Website Chatbot is an intelligent application that processes website data to provide highly accurate, context-aware answers to user queries. The application utilizes a custom intent classifier and local vector storage to instantly retrieve relevant document chunks and generate precise responses based on the crawled website content.

## Getting Started

To run the application, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone git@github.com:gunavardhangolagani/Sagex-website-chatbot.git
   ```
2. Navigate to the project directory:

    ```bash
    cd Sagex-website-chatbot
    ```

3. Navigate to the backend directory and install the required dependencies:
    ```bash
    cd backend
    ```
    ```bash
    pip install -r requirements.txt
    ```
- Run the backend application:
  
    ```bash
    uvicorn main:app --reload
    ```
4. Open a new terminal, navigate to the frontend directory, and install the required dependencies:
    ```bash
    cd frontend
    ```
    ```bash
    npm install
    ```
5. Run the frontend development server:
    
    ```bash
    npm run dev
    ```
6. Open your web browser and go to the address provided by Vite (usually http://localhost:5173) to access the application.

## Usage
- Open the chatbot interface in your web browser.

- Enter a query or question regarding the company or website content into the chat input field.

- Click the send button or press Enter to submit your message.

- The application will instantly classify the intent of your message and search the processed website data.

- View the AI generated response, which is formulated using the retrieved contextual information.

import { useEffect, useRef, useState } from "react";
import ChatbotIcon from "./components/ChatbotIcon";
import ChatForm from "./components/ChatForm";
import ChatMessage from "./components/ChatMessage";
import { companyInfo } from "./companyInfo";

const suggestions = [
  "What services do you offer?",
  "Show contact information",
  "Tell me about the company",
  "What industries do you serve?",
  "How can I get started?"
];

const App = () => {
  const chatBodyRef = useRef();

  const [showChatbot, setShowChatbot] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(true);

  const [chatHistory, setChatHistory] = useState([
    {
      hideInChat: true,
      role: "system",
      text: companyInfo,
    },
  ]);

  // =========================
  // Suggestion Click Handler
  // =========================
  const handleSuggestionClick = (text) => {
    setShowSuggestions(false);

    const userMessage = { role: "user", text };
    const updatedHistory = [...chatHistory, userMessage];

    setChatHistory(updatedHistory);

    setTimeout(() => {
      setChatHistory((history) => [
        ...history,
        { role: "model", text: "Thinking..." }
      ]);

      generateBotResponse(updatedHistory);
    }, 100);
  };

  // =========================
  // AI Response (BACKEND CALL)
  // =========================
const generateBotResponse = async (history) => {
    const updateHistory = (text, sourceUrl = "", isError = false) => {
      setChatHistory((prev) => [
        ...prev.filter((msg) => msg.text !== "Thinking..."),
        { role: "model", text: text, source: sourceUrl, isError: isError }
      ]);
    };
    try {
      const latestUserMessage = history[history.length - 1].text;
      const cleanedHistory = history
        .filter(msg => msg.role !== "system" && msg.text !== "Thinking...")
        .map(({ role, text }) => ({ role, text }));
      const response = await fetch(`${import.meta.env.VITE_API_URL}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({question: latestUserMessage, chat_history: cleanedHistory}),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data?.detail || "Something went wrong!");
      }
      updateHistory(data.answer, data.source);
    } catch (error) {
      updateHistory(error.message, "", true);
    }
  };

  // =========================
  // Auto Scroll
  // =========================
  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTo({
        top: chatBodyRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [chatHistory]);

  return (
    <div className={`container ${showChatbot ? "show-chatbot" : ""}`}>

      {/* Toggle Button */}
      <button
        onClick={() => setShowChatbot((prev) => !prev)}
        id="chatbot-toggler"
      >
        <span className="material-symbols-rounded">mode_comment</span>
        <span className="material-symbols-rounded">close</span>
      </button>

      {/* Chatbot */}
      <div className="chatbot-popup">

        {/* Header */}
        <div className="chat-header">
          <div className="header-info">
            <ChatbotIcon />
            <h2 className="logo-text">Chatbot</h2>
          </div>

          <button
            onClick={() => setShowChatbot((prev) => !prev)}
            className="material-symbols-rounded"
          >
            keyboard_arrow_down
          </button>
        </div>

        {/* Chat Body */}
        <div ref={chatBodyRef} className="chat-body">

          {/* Greeting */}
          <div className="message bot-message">
            <ChatbotIcon />
            <div>
              <p className="message-text">
                Hey there 👋 <br /> How can I help you today?
              </p>

              <p className="quick-actions">QUICK ACTIONS</p>

              {showSuggestions && (
                <div className="suggestions">
                  {suggestions.map((item, index) => (
                    <button
                      key={index}
                      className="suggestion-chip"
                      onClick={() => handleSuggestionClick(item)}
                    >
                      {item}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Chat Messages */}
          {chatHistory.map((chat, index) => (
            <ChatMessage key={index} chat={chat} />
          ))}

        </div>

        {/* Footer */}
        <div className="chat-footer">
          <ChatForm
            chatHistory={chatHistory}
            setChatHistory={setChatHistory}
            generateBotResponse={generateBotResponse}
          />
        </div>

      </div>
    </div>
  );
};

export default App;
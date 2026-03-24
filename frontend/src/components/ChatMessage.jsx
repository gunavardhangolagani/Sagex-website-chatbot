import ChatbotIcon from "./ChatbotIcon";
import ReactMarkdown from "react-markdown";

const ChatMessage = ({ chat }) => {
  return (
    !chat.hideInChat && (
      <div className={`message ${chat.role === "model" ? "bot" : "user"}-message ${chat.isError ? "error" : ""}`}>
        {chat.role === "model" && <ChatbotIcon />}

        <div className="message-text">
          
          <ReactMarkdown
            components={{
              a: ({ node, ...props }) => (
                <a target="_blank" rel="noopener noreferrer" style={{color: "#4f7cff"}} {...props} />
              )
            }}
          >
            {chat.text}
          </ReactMarkdown>

          {chat.source && (
            <div style={{ marginTop: "10px", borderTop: "1px solid rgba(0,0,0,0.1)", paddingTop: "8px" }}>
              <a 
                href={chat.source} 
                target="_blank" 
                rel="noopener noreferrer" 
                style={{ 
                  color: "#00008B", 
                  textDecoration: "none", 
                  fontWeight: "600",
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "5px",
                  fontSize: "0.85rem",
                  background: "#e8efff",
                  padding: "6px 10px",
                  borderRadius: "6px"
                }}
              >
                <span className="material-symbols-rounded" style={{fontSize: "16px"}}>link</span> 
                Source Document
              </a>
            </div>
          )}

        </div>
      </div>
    )
  );
};

export default ChatMessage;
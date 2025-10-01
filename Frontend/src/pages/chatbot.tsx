import React, { useState, useRef, useEffect } from "react";
import { Zap} from "lucide-react"; // import any icons you like
interface ChatbotProps {
  setShowChatbot: React.Dispatch<React.SetStateAction<boolean>>;
}
interface Message {
  sender: "user" | "bot";
  text: string;
}

const Chatbot: React.FC<ChatbotProps> = ({ setShowChatbot }) => {
  const [messages, setMessages] = useState<Message[]>([
    { sender: "bot", text: "Hello 👋! I'm your biodiversity assistant. How can I help you?" },
  ]);
  const [input, setInput] = useState("");
  
  // 1. We replace the old ref with one for the chat container itself.
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // 2. This is the new, robust scrolling logic.
  // It directly manipulates the chat box's scroll position.
  useEffect(() => {
    if (chatContainerRef.current) {
      const { scrollHeight, clientHeight } = chatContainerRef.current;
      chatContainerRef.current.scrollTop = scrollHeight - clientHeight;
    }
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage: Message = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    setTimeout(() => {
      const botReplies = [
        "The most abundent known specie in this data set is Bathypelagic Fish.",
      ];
      const randomReply = botReplies[Math.floor(Math.random() * botReplies.length)];
      const botMessage: Message = { sender: "bot", text: randomReply };
      setMessages((prev) => [...prev, botMessage]);
    }, 800);

    setInput("");
  };

  return (
    <div className="w-full max-w-[1000px] mx-auto mt-6 bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 flex flex-col h-[500px]">
      {/* Header */}
      <div className="flex items-center justify-between text-xl font-bold text-white mb-4">
        <div className="flex items-center">
         <Zap className="mr-2 h-5 w-5 text-cyan-400" /> BioBot Chat
        </div>
        
        <button
          onClick={() => setShowChatbot(false)}
          className="text-white font-bold px-2 py-1 rounded hover:bg-blue-500"
        >
          ✕
        </button>
      </div>

      {/* 3. Attach the ref to the scrollable chat window div. */}
      <div 
        ref={chatContainerRef} 
        className="flex-1 overflow-y-auto space-y-3 mb-4 pr-2"
        onWheel={(e) => e.stopPropagation()} 
      >
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`p-3 rounded-xl max-w-[75%] break-words ${
              msg.sender === "user"
                ? "bg-cyan-500/30 text-white ml-auto"
                : "bg-white/20 text-white/90"
            }`}
          >
            {msg.text}
          </div>
        ))}
        {/* 4. The old empty div for scrolling is no longer needed. */}
      </div>

      {/* Input Box */}
      <div className="flex space-x-2 border-t border-white/20 pt-3">
        <input
          type="text"
          className="flex-1 bg-white/20 text-white placeholder-gray-300 border border-white/10 rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-400 backdrop-blur-sm"
          placeholder="Ask me about biodiversity..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              handleSend();
            }
          }}
        />
        <button
          className="bg-cyan-400/70 hover:bg-cyan-400 text-white px-4 py-2 rounded-xl transition"
          onClick={handleSend}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;

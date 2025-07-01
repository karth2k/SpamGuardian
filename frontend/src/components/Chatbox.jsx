import React, {useState} from "react";
import Message from "./Message"
import { useEffect, useRef } from "react";


export default function Chatbox(){
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const bottomRef = useRef(null);

    useEffect(() => {
    bottomRef.current?.scrollIntoView({behavior: "smooth"});
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim() || isLoading) return;
        const userMsg = {text: input, type: "user"};
        setMessages((prev) => [...prev, userMsg]);

        setInput("");

        const typingMsg = {text: "Thinking...", type: "bot", temp: true};
        setMessages((prev)=> [...prev, typingMsg]);
        setIsLoading(true);
        try {
            const res = await fetch("http://127.0.0.1:5000/predict", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({text: input}),
            });

            const data = await res.json();
            const botMsg = {
                text: `${data.label}`,
                type: "bot",
            }
            setMessages((prev) => [...prev.filter(msg => !msg.temp), botMsg]);  
        }
        catch (err){
            setMessages((prev) => [...prev.filter(msg => !msg.temp), {text: "Error reaching server", type: "bot"}]);
        }
        finally{
            setIsLoading(false);
        }
        
    };

    const handleKeyDown = (e) => {
        if(e.key === "Enter") sendMessage();
    };


    return(
        <div style={{ backgroundColor: "#020617"}} className="flex flex-col h-screen p-4 text-white">
            <h1 className="text-xl font-semibold mb-4">Spam Guardian</h1>
            <div className = "flex-1 overflow-y-auto mb-4 border p-4 rounded">
                {messages.map((msg, idx)=> (
                    <Message key = {idx} text = {msg.text} type = {msg.type} isTemp = {msg.temp}></Message>
                ))}
                <div ref={bottomRef} />
            </div>
            <div className="flex">
                <input value={input} onChange = {(e)=>setInput(e.target.value)}
                onKeyDown = {handleKeyDown} placeholder="Enter text here to check if its spam..."
                className="flex-1 border px-4 py-2 rounded-l"/>
                <button disabled = {isLoading} onClick={sendMessage} className={`px-4 py-2 rounded-r ${isLoading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-500 text-white"}`}>
                    Send
                </button>
            </div>
        </div>
    );
}
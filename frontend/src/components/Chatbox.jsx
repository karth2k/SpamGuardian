import React, {useState} from "react";
import Message from "./Message"
import { useEffect, useRef } from "react";


export default function Chatbox(){
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");

    const bottomRef = useRef(null);

    useEffect(() => {
    bottomRef.current?.scrollIntoView({behavior: "smooth"});
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim()) return;
        const userMsg = {text: input, type: "user"};
        setMessages((prev) => [...prev, userMsg]);

        setInput("");

        try {
            const res = await fetch("http://localhost:5000/predict", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({text: input}),
            });

            const data = await res.json();
            const botMsg = {
                text: `Label: ${data.label}`,
                type: "bot",
            }
            setMessages((prev) => [...prev, botMsg]);  
        }
        catch (err){
            setMessages((prev) => [...prev, {text: "Error reaching server", type: "bot"}]);
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
                    <Message key = {idx} text = {msg.text} type = {msg.type}></Message>
                ))}
                <div ref={bottomRef} />
            </div>
            <div className="flex">
                <input value={input} onChange = {(e)=>setInput(e.target.value)}
                onKeyDown = {handleKeyDown} placeholder="Enter text here to check if its spam..."
                className="flex-1 border px-4 py-2 rounded-l"/>
                <button onClick={sendMessage} className="bg-blue-500 text-white px-4 py-2 rounded-r">
                    Send
                </button>
            </div>
        </div>
    );
}
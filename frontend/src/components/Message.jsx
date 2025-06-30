import React from "react";

export default function Message({text, type}){
    const isUser = type === "user";
    return(
        <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-3`}>
            <div className = {`rounded-2xl px-4 py-2 max-w-xs shadow ${isUser ? "bg-blue-500 text-white" : "bg-gray-200 text-black"}`}>
                {text}
            </div>
        </div>
    );
}
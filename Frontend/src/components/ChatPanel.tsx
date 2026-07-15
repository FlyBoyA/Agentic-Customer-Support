import {useState} from "react";
import ChatMessage from "./ChatMessage";
import QuickQuestions from "./QuickQuestion";
import type {Message} from "../types/agent";


interface Props {
  messages: Message[];
  loading: boolean;
  onSend: (question:string)=>void;
}

export default function ChatPanel({messages,loading,onSend}:Props){
const [question,setQuestion]=useState("");

function send(){
if(!question.trim()) return;
 onSend(question);
 setQuestion("");
}



return (<div className="bg-white rounded-xl shadow p-6">


<h2 className="text-xl font-semibold mb-4">
 Chat with Agent
</h2>

<div className="h-[420px] overflow-y-auto bg-gray-50 rounded-lgp-4">
{messages.map(message=>(<ChatMessage key={message.id} message={message}/>))}
{loading && (<div className=" text-gray-500 animate-pulse"> Thinking...

</div>
)}

</div>

<div className="flex gap-2 mt-4">

<input value={question} onChange={ e=>setQuestion(e.target.value)} onKeyDown={e=>{if(e.key==="Enter")send()}} placeholder="Type your question..." className="flex-1border rounded-lg px-4 py-2"/>


<button onClick={send} className="bg-indigo-500 text-white px-6 rounded-lg ">
Send
</button>

</div>
<QuickQuestions onAsk={onSend}/>
</div>
)}
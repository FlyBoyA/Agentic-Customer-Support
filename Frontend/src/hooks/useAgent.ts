import {useState} from "react";
import {askAgent, getHealth, resetAgent} from "../api/agentApi";
import type { Message } from "../types/agent";


export function useAgent(){
const [messages,setMessages]=useState<Message[]>([{id:1, role:"bot", content:"Welcome! Ask me about accounts, billing, integrations, or security."}]);
const [loading,setLoading]=useState(false);
const [stats,setStats]=useState({documents:0,count:0,action:"-",confidence:"-"});
const [logs,setLogs]=useState<string[]>([]);

function addLog(text:string){
 setLogs(prev=>[ ...prev, `[${new Date().toLocaleTimeString()}] ${text}`]);

}

async function sendQuestion(question:string){if(!question.trim()) return;
setMessages(prev=>[ ...prev,{id:Date.now(), role:"user",content:question}]);
setLoading(true);

try{

 const start=performance.now();
 const data=await askAgent(question);
 const latency=((performance.now()-start)/1000).toFixed(2);

setMessages(prev=>[ ...prev, {id:Date.now(), role:"bot", content:data.response,data }]);

setStats(prev=>({ ...prev, count:prev.count+1,action:data.action, confidence: data.confidence ? `${(data.confidence*100).toFixed(0)}%` : "-" }));

addLog( `Action: ${data.action}, latency ${latency}s`);
}
catch(error){

setMessages(prev=>[ ...prev, { id:Date.now(), role:"bot", content: " Could not connect to server" }]);
addLog("ERROR: Server unavailable");
}

setLoading(false);

}

async function loadStatus(){
try{

const data=await getHealth();

setStats(prev=>({ ...prev, documents:data.vector_store_count}));
addLog(`System healthy. ${data.vector_store_count} documents loaded`);

}catch{

addLog("ERROR: Backend offline");
}
}

async function reset(){

await resetAgent();
setMessages([]);
addLog("Agent reset");
}



return { messages, loading, stats, logs, sendQuestion, loadStatus, reset};

}
import type {Message} from "../types/agent";


export default function ChatMessage({message}:{message:Message}){

return (

<div className={`mb-3 p-3 rounded-xl max-w-[85%]

${message.role==="user" ? "ml-auto bg-indigo-500 text-white" : "bg-indigo-100 text-gray-800"}`}>

{message.data && <div className="text-xs mb-2">
{message.data.action==="answer" && "Answer"}
{message.data.action==="clarify" && "Clarifying"}
{message.data.action==="decline" && "Declined"}

</div>
}

{message.content}

</div>
)}
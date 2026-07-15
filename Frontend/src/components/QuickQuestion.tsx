const questions=["password", "refund","subscription","data storage"];


export default function QuickQuestions({onAsk}:{onAsk:(q:string)=>void}){

return (

<div className="flex flex-wrap gap-2 mt-4">

{questions.map(q=>(<button key={q}
onClick={()=>onAsk(q)}
className="px-3 py-1 rounded-full bg-gray-200 hover:bg-indigo-500 hover:text-white text-sm">
{q}
</button>
))}

</div>
)}
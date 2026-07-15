interface Props{
logs:string[];
}


export default function DebugLog({logs}:Props){


return (<div className="bg-black text-green-400 rounded-xl p-4 h-[250px] overflow-y-auto font-mono text-sm">

<h3 className="text-white mb-3">
 Debug Log
</h3>

{logs.length===0 ?
<div> 
    System ready...
</div> : logs.map((log,index)=>(<div key={index}> {log}</div>))}</div>)}
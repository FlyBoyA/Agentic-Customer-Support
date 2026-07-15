interface Props {

stats:{
    documents:number;
    count:number;
    action:string;
    confidence:string;
};

onReset:()=>void;

}

export default function StatusPanel({stats,onReset}:Props){

return (
<div className="space-y-5">

<div className="bg-white rounded-xl shadow p-6">


<h2 className="text-xlfont-semiboldmb-4">
System Status
</h2>

<div className="gridgrid-cols-2gap-3">

<Stat label="Knowledge Base"value={stats.documents}/>

<Stat label="Messages" value={stats.count}/>

<Stat label="Last Action"value={stats.action}/>

<Stat label="Confidence" value={stats.confidence}/>

</div>
<button onClick={onReset} className="mt-5 bg-orange-500 text-white px-4 py-2 rounded-lg">

 Reset Agent

</button>


</div>


</div>

)

}



function Stat({label,value}:{label:string; 
    value:string|number;}){


return (

<div className="bg-gray-100 rounded-lg p-4 text-center">

<div className=" text-2xlfont-bold ">

{value}

</div>


<div className="text-xstext-gray-500">

{label}

</div>


</div>

)

}
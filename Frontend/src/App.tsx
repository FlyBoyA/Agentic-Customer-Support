import Header from "./components/Header";
import ChatPanel from "./components/ChatPanel";
import StatusPanel from "./components/StatusPanel";
import DebugLog from "./components/DebugLog";

import {useAgent} from "./hooks/useAgent";
import {useEffect} from "react";


function App(){

const {messages,loading,stats,logs,sendQuestion,loadStatus,reset}=useAgent();

useEffect(()=>{ loadStatus();
},[]);



return ( <div className="min-h-screen bg-gray-100">

<Header />



<main className="max-w-6xl mx-auto p-6">

<div className="grid md:grid-cols-3 gap-6">




<div className="md:col-span-2">

<ChatPanel

messages={messages}

loading={loading}

onSend={sendQuestion}

/>

</div>




<div>


<StatusPanel stats={stats} onReset={reset}/>



<div className="mt-5">

<DebugLog logs={logs}/>

</div>

</div>


</div>

</main>

</div>

)}


export default App;
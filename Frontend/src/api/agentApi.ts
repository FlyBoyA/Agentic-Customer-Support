const API_URL = "http://localhost:8000/api/v1";

export async function askAgent(question:string){

    const response = await fetch(
        `${API_URL}/ask`,
        {
            method:"POST",
            headers:{ "Content-Type":"application/json" },
            body:JSON.stringify({question})
        }
    );

    return response.json();
}


export async function getHealth(){
    const response = await fetch(`${API_URL}/health`);
    return response.json();
}

export async function resetAgent(){

 const response = await fetch(
    `${API_URL}/reset`,
    {
      method:"POST"
    }
 );

 return response.json();

}
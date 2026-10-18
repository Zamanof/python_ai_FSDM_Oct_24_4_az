const API = "http://localhost:5220";

export type PredictIn={
    bedrooms:number,
    bathrooms:number,
    sqm:number,
    city:string,
}

export async function predict(data:PredictIn){
    const response =
        await fetch(`${API}/api/AI/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });
    if (!response.ok) {
        throw new Error(`HTTP status ${response.status} - ${response.statusText}`);
    }
    return response.json() as Promise<{priceAzn:number}>;
}
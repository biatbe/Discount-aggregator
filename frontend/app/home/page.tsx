'use client';

import { useEffect, useState } from "react"


export default function Home() {

  const [results, setResults] = useState<any>([{}]);

  useEffect(() => {
    fetch("http://localhost:8080/api/products", {
      cache: "no-cache"
    }).then((res) => res.json())
    .then(data => {
      setResults(data);
      console.log(data);
    });
  },[])



  return (
    <>
      <div className="flex flex-wrap">
        {results != null && results.length > 0 ? (
          results.map((result : any) => (
            <div key={result.id}>
              <h1>{result.brand}</h1>
              <div>{result.name}</div>
              <div className="line-through">{result.oldPrice}</div>
              <div>{result.price}</div>
              <div>{result.displayDiscountPercentage}%</div>
              <div>
                <img width="250" src={result.url}/></div>
            </div>
          ))
        ) : (
          <p>Loading...</p>
        )}
      </div>
    </>
  )
}
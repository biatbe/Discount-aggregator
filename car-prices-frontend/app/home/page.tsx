'use client';

import { useEffect, useState } from "react"


export default function Home() {

  const [data, setData] = useState<any>([{}]);

  useEffect(() => {
    fetch("/cars", {
      cache: "no-cache"
    }).then((res) => res.json())
    .then(data => {
      setData(data);
      console.log(data);
    });
  },[])


  return (
    <>
      <div>

        {(typeof data.cars === "undefined") ? (
          <p>Loading...</p>
        ) : (
          data.cars.map((car : string, i : number) => (
            <p key={i}>{car}</p>
          ))
        )}
        
      </div>
    </>
  )
}
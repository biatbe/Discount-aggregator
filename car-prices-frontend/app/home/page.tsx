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

        {(data.make == null) ? (
          <p>Loading...</p>
        ) : (
          <p>{data.make}</p>
        )}
        
      </div>
    </>
  )
}
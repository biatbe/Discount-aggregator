'use client';

import { useEffect, useState } from "react"


export default function Home() {

  const [data, setData] = useState<any>([{}]);

  // useEffect(() => {
  //   fetch("/cars", {
  //     cache: "no-cache"
  //   }).then((res) => res.json())
  //   .then(data => {
  //     setData(data);
  //     console.log(data);
  //   });
  // },[])

  // useEffect(() => {
  //   search();
  // },[])

  const search = async () => {
    const response = await fetch("/api/search/mobile_de", {
      method: "POST",
      headers: { 
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({_type: "car", make: "Ford", model: "Kuga", maximum_km: 500, body_type: "suv",
         eqLevel: "ST LINE X", combustion: "plug_in", power_min: 224, power_max: 251, transmission: "automatic", first_reg: 2024}),
    })

    const prices = await response.json();
    setData(prices)
  }


  return (
    <>
      <div>
        <button type="button" onClick={search}>Search</button>
        {(data.make == null) ? (
          <p>Loading...</p>
        ) : (
          <p>{data.make}</p>
        )}
        
      </div>
    </>
  )
}
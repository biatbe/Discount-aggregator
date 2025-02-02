'use client';

import { useEffect, useState } from "react"
import ProductLayout from "../components/product_layout";


interface Product {
  brand: string,
  displayDiscountPercentage: number,
  id: number,
  name: string,
  oldPrice: number,
  price: number,
  sectionName: string,
  url: string,
  href: string
}

export default function Home() {

  const [results, setResults] = useState<Product[]>([]);

  useEffect(() => {
    fetch("http://localhost:8080/api/products")
      .then((res) => res.json())
        .then(data => {
          setResults(data);
          console.log(data);
        });
  },[])



  // Only showing the first 100 results for now.
  return (
    <>
      <div className="flex flex-wrap">
        {results != null && results.length > 0 ? (
          <ProductLayout products={results.slice(0, 100)} />
        ) : (
          <p>Loading...</p>
        )}
      </div>
    </>
  )
}
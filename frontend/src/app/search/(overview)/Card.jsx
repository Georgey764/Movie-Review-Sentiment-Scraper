"use client";

import axios from "axios";
import { useEffect, useState } from "react";

export default function Card({ movieName }) {
  const [result, setResult] = useState("loading...");
  const url = `http://localhost:8080/get_sentiment?q=${encodeURIComponent(
    movieName
  )}`;

  useEffect(() => {
    setResult("loading...");
    const res = axios
      .get(url)
      .then((res) => {
        console.log(res);
        setResult("Set");
      })
      .catch((error) => {
        console.log(error);
        setResult("Error");
      });
  }, [movieName]);

  return (
    <div className="flex flex-row align-center justify-center">{result}</div>
  );
}

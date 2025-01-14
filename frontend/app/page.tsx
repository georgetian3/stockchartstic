"use client"

import { useEffect, useState } from "react";
import { Bar, CartesianGrid, ErrorBar, Line, LineChart, Tooltip, XAxis, YAxis } from "recharts";


interface OHLCV {
  timestamp: Date
  open: number | null
  high: number | null
  low: number | null
  close: number | null
  volume: number | null
}


export default function Home() {


  const [data, setData] = useState<OHLCV[]>([])

  useEffect(() => {
    fetch('http://localhost:8000/aapl').then(
      (value) => {
        value.json().then(
          (value) => {
            setData(value)
          }
        )
      }
    )
  }, [])

  console.log(data)

  return <LineChart width={1200} height={800} data={data}>
    <XAxis dataKey="timestamp" />
    <Bar barSize={30} xAxisId={0}  dataKey="open" fill="#035aa6" />
    {/* <Bar barSize={35} xAxisId={1} dataKey="close" fill="white">
      <ErrorBar  dataKey="high" width={4} strokeWidth={2} stroke="#66c208" />
      <ErrorBar dataKey="low" width={4} strokeWidth={2} stroke="#ff0044" />
    </Bar> */}
  </LineChart>
    
}

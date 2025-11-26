"use client"

import { useEffect, useState } from "react";

import ReactECharts, { EChartsOption } from 'echarts-for-react';


interface BarList {
  timestamp: Date[]
  open: number[]
  high: number[]
  low: number[]
  close: number[]
  volume: number[]
  trade_count: number[]
  vwap: number[]
}

const emptyBarList: BarList = {
  timestamp: [],
  open: [],
  high: [],
  low: [],
  close: [],
  volume: [],
  trade_count: [],
  vwap: [],
}

function min(arr: number[]) {
  let min = Number.POSITIVE_INFINITY
  for (const elem of arr) {
    if (elem < min) {
      min = elem
    }
  }
  return min
}

function max(arr: number[]) {
  let max = Number.NEGATIVE_INFINITY
  for (const elem of arr) {
    if (elem > max) {
      max = elem
    }
  }
  return max
}

export default function Home() {


  const [data, setData] = useState<BarList>(emptyBarList)

  useEffect(() => {
    fetch('http://localhost:8000/bars?symbol=AAPL&start=2024-01-30T12:00:00&end=2025-01-30T21:00:00').then(
      (value) => {
        value.json().then(
          (json) => {
            console.log('json', json)
            json.timestamp = json.timestamp.map((t: string) => new Date(t))
            setData(json)
            // console.log(data.timestamp)
            
          }
        )
      }
    )
  }, [])

  console.log('data', data)

  const option: EChartsOption = {
    xAxis: {
      // type: 'time',
      data: data.timestamp
    },
    yAxis: {
      min: Math.floor(min(data.low)),
      max: Math.ceil(max(data.high))
    },
    series: [
      {
        type: 'candlestick',
        data: data.open.map((_, i) => [data.close[i], data.open[i], data.low[i], data.high[i]]),
      }
    ]
  };


  return <ReactECharts opts={{renderer: 'svg'}} option={option} style={{height: '1000px'}}/>;
    
}

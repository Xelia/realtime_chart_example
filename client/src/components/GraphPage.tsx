import React, { useEffect, useState } from "react";
import Graph from "./Graph.tsx";

const GraphPage = () => {
  const [tickers, setTickers] = useState([]);
  const [selectedTicker, setSelectedTicker] = useState("ticker_00");

  useEffect(() => {
    const fetchData = async () => {
      const result = await fetch("/api/tickers");
      const data = await result.json();
      console.log(result);
      setTickers(data);
    };

    fetchData();
  }, []);

  return (
    <>
      <div className="field">
        <label className="label">Тикер</label>
        <div className="control">
          <div className="select">
            <select onChange={(e) => setSelectedTicker(e.target.value)}>
              {tickers.map((value) => {
                return (
                  <option value={value} key={value}>
                    {value}
                  </option>
                );
              })}
            </select>
          </div>
        </div>
      </div>
      <Graph ticker={selectedTicker}></Graph>
    </>
  );
};

export default GraphPage;

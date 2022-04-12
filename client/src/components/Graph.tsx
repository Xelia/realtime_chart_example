import React, { useEffect, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

interface GraphProps {
  ticker: string;
}

const Graph = ({ ticker }: GraphProps) => {
  const [data, setData] = useState([]);
  const { sendMessage, lastMessage, readyState } = useWebSocket(
    "ws://" + window.location.host + "/api/ws"
  );

  useEffect(() => {
    if (readyState == ReadyState.OPEN) {
      sendMessage(JSON.stringify({ ticker }));
    }
    setData([]);
  }, [readyState, ticker]);

  useEffect(() => {
    if (lastMessage) {
      const messageData = JSON.parse(lastMessage.data);
      setData(data.concat(messageData.data));
    }
  }, [lastMessage]);

  return (
    <>
      <h1 className="title" style={{ textAlign: "center" }}>
        {ticker}
      </h1>
      <div style={{ width: "100%", height: "300px" }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart width={500} height={300} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis />
            <YAxis />
            <Line
              type="monotone"
              dataKey={(v) => v}
              isAnimationActive={false}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </>
  );
};

export default Graph;

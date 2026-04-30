"use client";

import { useEffect, useState } from "react";
import { getQueue } from "@/lib/api";

export default function QueuePage() {
  const [items, setItems] = useState<any[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getQueue()
      .then(setItems)
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Failed to load queue")
      );
  }, []);

  if (error) {
    return <p className="text-red-600">{error}</p>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Queue</h1>

      <div className="overflow-hidden rounded-xl border bg-white shadow-sm">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-100 text-left">
            <tr>
              <th className="px-4 py-3">ID</th>
              <th className="px-4 py-3">Email ID</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">Attempts</th>
              <th className="px-4 py-3">Error</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id} className="border-t">
                <td className="px-4 py-3">{item.id}</td>
                <td className="px-4 py-3">{item.email_id}</td>
                <td className="px-4 py-3">
                  <span
                    className={
                      item.status === "pending"
                        ? "text-yellow-600"
                        : item.status === "processing"
                        ? "text-blue-600"
                        : item.status === "failed"
                        ? "text-red-600"
                        : "text-green-600"
                    }
                  >
                    {item.status}
                  </span>
                </td>
                <td className="px-4 py-3">{item.attempts}</td>
                <td className="px-4 py-3">{item.last_error || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

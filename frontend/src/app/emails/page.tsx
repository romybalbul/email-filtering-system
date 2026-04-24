"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getEmails } from "@/lib/api";
import type { StoredEmail } from "@/lib/types";

export default function EmailsPage() {
  const [emails, setEmails] = useState<StoredEmail[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getEmails()
      .then(setEmails)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load emails"));
  }, []);

  if (error) {
    return <p className="text-red-600">{error}</p>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Emails</h1>

      <div className="overflow-hidden rounded-xl border bg-white shadow-sm">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-100 text-left">
            <tr>
              <th className="px-4 py-3">ID</th>
              <th className="px-4 py-3">Sender</th>
              <th className="px-4 py-3">Recipient</th>
              <th className="px-4 py-3">Subject</th>
              <th className="px-4 py-3">Score</th>
              <th className="px-4 py-3">Verdict</th>
            </tr>
          </thead>
          <tbody>
            {emails.map((email) => (
              <tr key={email.id} className="border-t">
                <td className="px-4 py-3">
                  <Link href={`/emails/${email.id}`} className="text-blue-600 hover:underline">
                    {email.id}
                  </Link>
                </td>
                <td className="px-4 py-3">{email.sender}</td>
                <td className="px-4 py-3">{email.recipient}</td>
                <td className="px-4 py-3">{email.subject || "-"}</td>
                <td className="px-4 py-3">{email.score}</td>
                <td className="px-4 py-3">{email.verdict}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

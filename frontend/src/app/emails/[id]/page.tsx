import Link from "next/link";
import { getEmailById } from "@/lib/api";

export default async function EmailDetailsPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const email = await getEmailById(id);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <Link href="/emails" className="text-sm text-blue-600 hover:underline">
            ← Back to Emails
          </Link>
          <h1 className="mt-2 text-3xl font-bold">Email #{email.id}</h1>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-xl border bg-white p-5 shadow-sm">
          <h2 className="text-lg font-semibold">Metadata</h2>
          <div className="mt-4 space-y-2 text-sm">
            <p><span className="font-medium">Sender:</span> {email.sender}</p>
            <p><span className="font-medium">Recipient:</span> {email.recipient}</p>
            <p><span className="font-medium">Subject:</span> {email.subject || "-"}</p>
            <p><span className="font-medium">Score:</span> {email.score}</p>
            <p><span className="font-medium">Verdict:</span> {email.verdict}</p>
            <p><span className="font-medium">Created:</span> {new Date(email.created_at).toLocaleString()}</p>
          </div>
        </div>

        <div className="rounded-xl border bg-white p-5 shadow-sm">
          <h2 className="text-lg font-semibold">Body</h2>
          <p className="mt-4 whitespace-pre-wrap text-sm text-gray-700">
            {email.body || "No body"}
          </p>
        </div>
      </div>

      <div className="rounded-xl border bg-white p-5 shadow-sm">
        <h2 className="text-lg font-semibold">Rule Hits</h2>

        {email.rule_hits.length === 0 ? (
          <p className="mt-4 text-sm text-gray-500">No rule hits recorded.</p>
        ) : (
          <div className="mt-4 overflow-hidden rounded-lg border">
            <table className="min-w-full text-sm">
              <thead className="bg-gray-100 text-left">
                <tr>
                  <th className="px-4 py-3">Rule</th>
                  <th className="px-4 py-3">Score Delta</th>
                  <th className="px-4 py-3">Reason</th>
                </tr>
              </thead>
              <tbody>
                {email.rule_hits.map((hit) => (
                  <tr key={hit.id} className="border-t">
                    <td className="px-4 py-3">{hit.rule_name}</td>
                    <td className="px-4 py-3">{hit.score_delta}</td>
                    <td className="px-4 py-3">{hit.reason || "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

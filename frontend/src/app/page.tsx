import Link from "next/link";

export default function HomePage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Email Filtering Admin</h1>
        <p className="mt-2 text-gray-600">
          Simple admin UI for browsing filtered emails and managing DB-backed lists.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Link
          href="/emails"
          className="rounded-xl border bg-white p-6 shadow-sm transition hover:shadow"
        >
          <h2 className="text-xl font-semibold">Emails</h2>
          <p className="mt-2 text-sm text-gray-600">
            Browse saved emails, verdicts, scores, and rule hits.
          </p>
        </Link>

        <Link
          href="/lists"
          className="rounded-xl border bg-white p-6 shadow-sm transition hover:shadow"
        >
          <h2 className="text-xl font-semibold">Lists</h2>
          <p className="mt-2 text-sm text-gray-600">
            Manage trusted domains, blocked senders, and blocked extensions.
          </p>
        </Link>
      </div>
    </div>
  );
}

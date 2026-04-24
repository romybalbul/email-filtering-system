"use client";

import { useEffect, useState } from "react";
import { addListEntry, deleteListEntry, getListEntries } from "@/lib/api";
import type { ListEntry } from "@/lib/types";

type Props = {
  listType: "trusted_domains" | "blocked_senders" | "blocked_extensions" | "blocked_ips" | "relay_allowed_ips" | "local_domains";
  title: string;
};

export default function ListManager({ listType, title }: Props) {
  const [entries, setEntries] = useState<ListEntry[]>([]);
  const [value, setValue] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function loadEntries() {
    try {
      setLoading(true);
      setError("");
      const data = await getListEntries(listType);
      setEntries(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load entries");
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!value.trim()) return;

    try {
      setSubmitting(true);
      setError("");
      await addListEntry(listType, value);
      setValue("");
      await loadEntries();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add entry");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleDelete(entryId: number) {
    try {
      setError("");
      await deleteListEntry(listType, entryId);
      await loadEntries();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete entry");
    }
  }

  useEffect(() => {
    loadEntries();
  }, [listType]);

  return (
    <div className="rounded-xl border bg-white p-5 shadow-sm">
      <h2 className="text-lg font-semibold">{title}</h2>

      <form onSubmit={handleSubmit} className="mt-4 flex gap-2">
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder={`Add to ${listType}`}
          className="flex-1 rounded-lg border px-3 py-2 text-sm"
        />
        <button
          type="submit"
          disabled={submitting}
          className="rounded-lg border bg-gray-900 px-4 py-2 text-sm text-white disabled:opacity-50"
        >
          Add
        </button>
      </form>

      {error ? <p className="mt-3 text-sm text-red-600">{error}</p> : null}

      {loading ? (
        <p className="mt-4 text-sm text-gray-500">Loading...</p>
      ) : (
        <div className="mt-4 space-y-2">
          {entries.length === 0 ? (
            <p className="text-sm text-gray-500">No entries yet.</p>
          ) : (
            entries.map((entry) => (
              <div
                key={entry.id}
                className="flex items-center justify-between rounded-lg border px-3 py-2 text-sm"
              >
                <span>{entry.value}</span>
                <button
                  onClick={() => handleDelete(entry.id)}
                  className="text-red-600 hover:underline"
                >
                  Delete
                </button>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

import type { EmailDetails, ListEntry, StoredEmail } from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access_token");
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getToken();

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(init?.headers || {}),
    },
    cache: "no-store",
  });

  if (response.status === 401 && typeof window !== "undefined") {
    localStorage.removeItem("access_token");
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API error ${response.status}: ${text}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

export async function getEmails(): Promise<StoredEmail[]> {
  return apiFetch<StoredEmail[]>("/emails");
}

export async function getEmailById(id: string): Promise<EmailDetails> {
  return apiFetch<EmailDetails>(`/emails/${id}`);
}

export async function getListEntries(listType: string): Promise<ListEntry[]> {
  return apiFetch<ListEntry[]>(`/lists/${listType}`);
}

export async function addListEntry(
  listType: string,
  value: string
): Promise<ListEntry> {
  return apiFetch<ListEntry>(`/lists/${listType}`, {
    method: "POST",
    body: JSON.stringify({ value }),
  });
}

export async function deleteListEntry(
  listType: string,
  entryId: number
): Promise<void> {
  return apiFetch<void>(`/lists/${listType}/${entryId}`, {
    method: "DELETE",
  });
}

export async function getQueue() {
  return apiFetch<any[]>("/queue");
}

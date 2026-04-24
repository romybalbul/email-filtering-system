import ListManager from "@/components/list-manager";

export default function ListsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Lists</h1>
        <p className="mt-2 text-gray-600">
          Manage DB-backed filtering lists used by the backend.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <ListManager
          listType="trusted_domains"
          title="Trusted Domains"
        />
        <ListManager
          listType="blocked_senders"
          title="Blocked Senders"
        />
      </div>

      <div className="grid gap-6 md:grid-cols-1">
        <ListManager
          listType="blocked_extensions"
          title="Blocked Extensions"
        />
      </div>
    </div>
  );
}

import ListManager from "@/components/list-manager";

export default function ListsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Lists</h1>
        <p className="mt-2 text-gray-600">
          Manage DB-backed filtering and SMTP access-control lists.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <ListManager listType="trusted_domains" title="Trusted Domains" />
        <ListManager listType="blocked_senders" title="Blocked Senders" />
        <ListManager listType="blocked_extensions" title="Blocked Extensions" />
        <ListManager listType="local_domains" title="Local Recipient Domains" />
        <ListManager listType="blocked_ips" title="Blocked SMTP IPs / CIDRs" />
        <ListManager listType="relay_allowed_ips" title="Relay Allowed IPs / CIDRs" />
      </div>
    </div>
  );
}

import "./globals.css";
import Link from "next/link";

export const metadata = {
  title: "Email Filtering System",
  description: "Admin UI for the email filtering system",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900">
        <div className="min-h-screen">
          <header className="border-b bg-white">
            <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
              <Link href="/" className="text-lg font-semibold">
                Email Filtering System
              </Link>

              <nav className="flex gap-4 text-sm">
                <Link href="/" className="hover:underline">
                  Dashboard
                </Link>
                <Link href="/emails" className="hover:underline">
                  Emails
                </Link>
                <Link href="/lists" className="hover:underline">
                  Lists
                </Link>
              </nav>
            </div>
          </header>

          <main className="mx-auto max-w-6xl px-6 py-8">{children}</main>
        </div>
      </body>
    </html>
  );
}

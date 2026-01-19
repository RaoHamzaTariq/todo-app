"use client";

import { useEffect, useState } from "react";
import { authClient } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Button from "./ui/Button";

export default function Navigation() {
  const router = useRouter();
  const [session, setSession] = useState<any>(null);
  const [isPending, setIsPending] = useState(true);

  useEffect(() => {
    let mounted = true;

    async function fetchSession() {
      const { data } = await authClient.getSession(); // fetch once
      if (mounted) {
        setSession(data);
        setIsPending(false);
      }
    }

    fetchSession();

    return () => {
      mounted = false;
    };
  }, []);

  const handleSignOut = async () => {
    await authClient.signOut();
    router.push("/sign-in");
  };

  return (
    <nav className="flex justify-between items-center" role="navigation" aria-label="Main navigation">
      <div className="flex items-center space-x-8">
        <Link href="/tasks" className="text-xl font-bold text-gray-900" aria-label="Todo App home">
          Todo App
        </Link>
        <div className="hidden md:flex space-x-6" role="menubar">
          <Link
            href="/tasks"
            className="text-gray-600 hover:text-gray-900 transition-colors"
            aria-label="View your tasks"
          >
            My Tasks
          </Link>
          <Link
            href="/tasks/new"
            className="text-gray-600 hover:text-gray-900 transition-colors"
            aria-label="Create a new task"
          >
            New Task
          </Link>
        </div>
      </div>

      {!isPending && session && (
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-600 hidden sm:inline" aria-label={`Welcome, ${session.user?.name}`}>
            Welcome, <span className="font-medium text-gray-900">{session.user?.name}</span>
          </span>
          <Button
            variant="ghost"
            onClick={handleSignOut}
            aria-label="Sign out"
          >
            Sign Out
          </Button>
        </div>
      )}
    </nav>
  );
}

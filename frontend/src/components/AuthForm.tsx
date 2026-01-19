"use client";

import { useState } from "react";
import { authClient } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import {Input} from "./ui/Input";
import {Button} from "./ui/Button";
import {Card} from "./ui/Card";

interface AuthFormProps {
  type: "sign-in" | "sign-up";
}

export default function AuthForm({ type }: AuthFormProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const isSignIn = type === "sign-in";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (isSignIn) {
        const { error } = await authClient.signIn.email({
          email,
          password,
          callbackURL: "/tasks",
        });
        if (error) throw new Error(error.message);
      } else {
        const { error } = await authClient.signUp.email({
          email,
          password,
          name,
          callbackURL: "/tasks",
        });
        if (error) throw new Error(error.message);
      }

      router.push("/tasks");
      router.refresh();
    } catch (err: any) {
      setError(err.message || "Authentication failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md">
      <h2 className="mb-6 text-2xl font-bold text-gray-900 text-center">
        {isSignIn ? "Sign In" : "Create Account"}
      </h2>

      {error && (
        <div className="mb-4 p-3 text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        {!isSignIn && (
          <Input
            label="Full Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="John Doe"
            required
          />
        )}

        <Input
          label="Email Address"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="name@example.com"
          required
        />

        <Input
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="••••••••"
          required
          minLength={8}
        />

        <Button
          type="submit"
          loading={loading}
          disabled={loading}
          variant="primary"
          className="w-full"
        >
          {loading ? "Processing..." : isSignIn ? "Sign In" : "Sign Up"}
        </Button>
      </form>

      <div className="mt-6 text-center text-sm text-gray-600">
        {isSignIn ? (
          <>
            Don't have an account?{" "}
            <a href="/sign-up" className="text-blue-600 hover:underline font-medium">Sign Up</a>
          </>
        ) : (
          <>
            Already have an account?{" "}
            <a href="/sign-in" className="text-blue-600 hover:underline font-medium">Sign In</a>
          </>
        )}
      </div>
    </Card>
  );
}

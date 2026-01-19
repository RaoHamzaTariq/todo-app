export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  betterAuthSecret: process.env.BETTER_AUTH_SECRET,
  databaseUrl: process.env.DATABASE_URL,
};

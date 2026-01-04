# Frontend Guidelines (Next.js App Router)

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   └── auth/
│   │   │       └── [...auth]/
│   │   │           └── route.ts
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── TaskForm.tsx
│   │   └── AuthForm.tsx
│   └── lib/
│       ├── auth.ts
│       └── api.ts
├── .env.local
├── next.config.js
├── package.json
└── tsconfig.json
```

## Technology Stack

- **Framework:** Next.js 16+ (App Router)
- **Styling:** Tailwind CSS
- **Authentication:** Better Auth
- **Language:** TypeScript

## Patterns

- Use server components by default
- Client components only when needed (interactivity)
- API calls go through `/lib/api.ts`

## Component Structure

- `/components` - Reusable UI components
- `/app` - Pages and layouts

## API Client

All backend calls should use the API client with JWT token:

```typescript
import { authClient } from "@/lib/auth-client";

async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const session = await authClient.getSession();

  if (!session?.data?.session) {
    throw new Error("Not authenticated");
  }

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${session.data.session.token}`,
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  return response.json();
}
```

## Better Auth Configuration

**Client-side configuration:**

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000",
});
```

**Server-side API route (Next.js App Router):**

```typescript
// app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

**Server auth instance:**

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: {
    provider: "postgres",
    url: process.env.DATABASE_URL!,
  },
  secret: process.env.BETTER_AUTH_SECRET!,
  emailAndPassword: {
    enabled: true,
  },
});
```

## Component and Styling Conventions

- Use functional components with TypeScript
- Leverage Tailwind CSS for styling
- Use `use client` directive for interactive components
- Follow the component folder structure in `src/components/`
- Use React Query or SWR for data fetching
- No inline styles
- Follow existing component patterns

## Development Workflow

1. Read relevant specs from `specs/ui/` for component requirements
2. Read API specs from `specs/api/` for endpoint contracts
3. Implement components following the design specs
4. Test components with the FastAPI backend

## Environment Variables

```env
BETTER_AUTH_SECRET=your-secret-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running

```bash
cd frontend && npm run dev
```

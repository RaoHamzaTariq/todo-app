# Frontend Guidelines (Next.js App Router)

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth/
│   │   │   │   └── [...auth]/
│   │   │   │       └── route.ts
│   │   │   └── tasks/
│   │   │       ├── route.ts
│   │   │       └── [id]/
│   │   │           ├── route.ts
│   │   │           └── complete/
│   │   │               └── route.ts
│   │   ├── (auth)/
│   │   │   ├── sign-in/
│   │   │   │   └── page.tsx
│   │   │   └── sign-up/
│   │   │       └── page.tsx
│   │   ├── tasks/
│   │   │   ├── page.tsx
│   │   │   ├── new/
│   │   │   │   └── page.tsx
│   │   │   └── [id]/
│   │   │       ├── page.tsx
│   │   │       └── edit/
│   │   │           └── page.tsx
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── TaskForm.tsx
│   │   ├── AuthForm.tsx
│   │   ├── Header.tsx
│   │   └── ui/                  # Shared UI components (Button, Input, etc.)
│   └── lib/
│       ├── auth-client.ts
│       └── config.ts
├── .env.local
├── next.config.js
├── package.json
└── tsconfig.json
```
(Note: This is just basic structure, you can modify it if needed and expanded it more for more features and advanced application
)

## Technology Stack

- **Framework:** Next.js 16+ (App Router)
- **Styling:** Tailwind CSS
- **Authentication:** Better Auth
- **Language:** TypeScript

## Patterns

- Use server components by default
- Client components only when needed (interactivity)
- API calls go through Next.js API routes in `/app/api/`

## Component Structure

- `/components` - Reusable UI components
- `/app` - Pages and layouts
- `/app/api` - Next.js API routes

## Website UI Guidelines

### Responsive Design
- Mobile-first approach with responsive breakpoints
- Support for mobile, tablet, and desktop viewports
- Touch-friendly controls and adequate tap targets
- Responsive navigation patterns

### Accessibility (a11y)
- Semantic HTML structure
- Proper heading hierarchy (h1, h2, h3, etc.)
- ARIA labels and roles where appropriate
- Keyboard navigation support
- Sufficient color contrast ratios
- Focus indicators for interactive elements

### User Experience (UX)
- Clear visual hierarchy and information architecture
- Consistent design patterns throughout the application
- Loading states and skeleton screens for better perceived performance
- Form validation with clear error messaging
- Confirmation dialogs for destructive actions (deletion)
- Success feedback for user actions

### Navigation
- Intuitive navigation with clear breadcrumbs
- Consistent header/navigation across pages
- Proper handling of authentication state in navigation
- Back button support and browser history management

### Forms
- Input validation with immediate feedback
- Clear labeling of form fields
- Appropriate input types for different data (email, password, etc.)
- Loading states during form submission
- Error handling and recovery

### Error Handling
- Graceful error states and recovery options
- User-friendly error messages
- Proper 404 and 500 error pages
- Network error handling with retry mechanisms

## Next.js API Routes

API calls should go through Next.js API routes which handle authentication and proxy to the backend:

```typescript
// Example API route in /app/api/tasks/route.ts
import { NextRequest } from 'next/server';
import { authClient } from '@/lib/auth-client';

export async function GET(request: NextRequest) {
  const token = await authClient.token();

  if (!token.data?.token) {
    return new Response(JSON.stringify({ error: 'Unauthorized' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Proxy request to backend with JWT
  const response = await fetch(`${process.env.BACKEND_API_URL}/api/tasks`, {
    headers: {
      'Authorization': `Bearer ${token.data.token}`,
      'Content-Type': 'application/json',
    },
  });

  const data = await response.json();
  return Response.json(data);
}

export async function POST(request: NextRequest) {
  const token = await authClient.token();
  const body = await request.json();

  if (!token.data?.token) {
    return new Response(JSON.stringify({ error: 'Unauthorized' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Proxy request to backend with JWT
  const response = await fetch(`${process.env.BACKEND_API_URL}/api/tasks`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token.data.token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  const data = await response.json();
  return Response.json(data);
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
- Use React Query or SWR for data fetching from Next.js API routes
- No inline styles
- Follow existing component patterns
- Use server components by default, client components only when interactivity is needed
- Implement proper loading and error boundaries for better UX

## Development Workflow

1. Read relevant specs from `specs/ui/` for component requirements
2. Read API specs from `specs/api/` for endpoint contracts
3. Implement Next.js API routes that proxy to the backend
4. Implement components following the design specs
5. Test components with the FastAPI backend through Next.js API routes

## Environment Variables

```env
BETTER_AUTH_SECRET=your-secret-key
NEXT_PUBLIC_API_URL=http://localhost:3000
BACKEND_API_URL=http://localhost:8000
DATABASE_URL=your-database-url
```

## Running

```bash
cd frontend && npm run dev
```

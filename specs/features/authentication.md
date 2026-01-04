# Feature: User Authentication

## User Stories

- As a user, I can sign up with email and password
- As a user, I can sign in with email and password
- As a user, I remain signed in across sessions
- As a user, I can sign out
- As an authenticated user, I can access the API with my JWT

## Acceptance Criteria

### Sign Up

- Email is required and must be valid format
- Password must meet minimum requirements (8+ characters)
- Email must be unique
- Account is created with users table
- Returns 201 on success
- Returns 400 for validation errors
- Returns 409 if email already exists

### Sign In

- Email and password required
- Validates credentials against database
- Returns JWT token on successful authentication
- Returns 401 for invalid credentials
- Returns 400 for missing fields

### Session Management

- JWT token issued upon login
- Token includes user_id and expiration
- Frontend stores token (cookie or secure storage)
- Token automatically sent with API requests
- Token expires after configured period (default: 7 days)

### Sign Out

- Clears session on frontend
- Token no longer valid for API calls
- Returns 200 on success

### API Authentication

- All task endpoints require valid JWT
- Token passed in header: `Authorization: Bearer <token>`
- Invalid/expired token returns 401
- Backend extracts user_id from token for scoping

## Better Auth Configuration

Better Auth handles:
- User registration
- Session creation
- JWT token generation
- Sign in/sign out flows

### Required Setup

**Server-side (Backend API Route Handler):**
```typescript
// app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

**Server Auth Instance:**
```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: {
    provider: "postgres", // or your database provider
    url: process.env.DATABASE_URL!,
  },
  secret: process.env.BETTER_AUTH_SECRET!,
  emailAndPassword: {
    enabled: true,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
  },
});
```

**Client-side (Frontend):**
```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000",
});
```

## Security Requirements

- Passwords hashed before storage
- JWT signed with shared secret
- Token expiration enforced
- User isolation enforced on all endpoints
- No sensitive data in token payload

## Environment Variables

```env
BETTER_AUTH_SECRET=your-256-bit-secret-key
```

## Related Specifications

- API Endpoints: `@specs/api/rest-endpoints.md`
- Database Schema: `@specs/database/schema.md`

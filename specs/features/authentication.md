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

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: process.env.DATABASE_URL,
  emailAndPassword: {
    enabled: true,
  },
  plugins: [
    // Optional plugins
  ],
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

import { NextRequest } from 'next/server';
import { auth } from '@/lib/auth';
import { SignJWT } from 'jose';

// Helper function to get user ID from session or token
async function getUserId(request: NextRequest) {
  // First try to get session from cookies (for browser)
  const session = await auth.api.getSession({
    headers: request.headers
  });

  let userId: string | undefined;
  let token: string | undefined;

  // If no session from cookies, try Bearer token
  if (!session?.session) {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader?.startsWith('Bearer ')) {
      return { error: 'Unauthorized', status: 401 };
    }

    token = authHeader.substring(7);

    // Verify the JWT token
    try {
      const verificationJWT = await auth.api.verifyJWT();

      userId = verificationJWT.payload?.sub;

      if (!userId) {
        return { error: 'User ID not found in token', status: 401 };
      }
    } catch (error) {
      return { error: 'Invalid or expired token', status: 401 };
    }
  } else {
    // Session from cookies
    userId = session.session?.userId || session.user?.id;
  }

  if (!userId) {
    return { error: 'Invalid session data', status: 401 };
  }

  return { userId, token };
}

// Helper function to mint a new JWT for backend communication
async function mintBackendToken(userId: string) {
  const secretValue = process.env.BETTER_AUTH_SECRET;
  if (!secretValue) {
    console.error("CRITICAL: BETTER_AUTH_SECRET is not set in environment variables!");
    throw new Error("Server misconfiguration");
  }
  const secret = new TextEncoder().encode(secretValue);
  return await new SignJWT({ sub: userId, user_id: userId })
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('1m') // Short-lived token for internal call
    .sign(secret);
}

// GET /api/chat/conversations
export async function GET(request: NextRequest) {
  try {
    const { userId, token, error, status } = await getUserId(request);

    if (error) {
      return Response.json({ error }, { status });
    }

    if (!userId) {
      return Response.json({ error: 'User ID not found' }, { status: 401 });
    }

    // Mint a new JWT for the backend communication
    const backendToken = await mintBackendToken(userId);

    // Call your FastAPI backend with the JWT token
    const backendUrl = process.env.BACKEND_API_URL || 'http://127.0.0.1:8000';
    const backendEndpoint = `${backendUrl}/api/${userId}/conversations`;

    const response = await fetch(backendEndpoint, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${backendToken}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorText = await response.text();

      let errorData;
      try {
        errorData = JSON.parse(errorText);
      } catch {
        errorData = { error: 'Backend request failed', details: errorText };
      }

      return Response.json(errorData, { status: response.status });
    }

    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    console.error('Error in GET /api/chat/conversations:', error);
    return Response.json({
      error: 'Internal server error',
      message: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}

// POST /api/chat/conversations
export async function POST(request: NextRequest) {
  try {
    const { userId, token, error, status } = await getUserId(request);

    if (error) {
      return Response.json({ error }, { status });
    }

    if (!userId) {
      return Response.json({ error: 'User ID not found' }, { status: 401 });
    }

    // Mint a new JWT for the backend communication
    const backendToken = await mintBackendToken(userId);

    const body = await request.json();

    // Call your FastAPI backend with the JWT token
    const backendUrl = process.env.BACKEND_API_URL || 'http://127.0.0.1:8000';
    const backendEndpoint = `${backendUrl}/api/${userId}/conversations`;

    const response = await fetch(backendEndpoint, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${backendToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorText = await response.text();

      let errorData;
      try {
        errorData = JSON.parse(errorText);
      } catch {
        errorData = { error: 'Backend request failed', details: errorText };
      }

      return Response.json(errorData, { status: response.status });
    }

    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    console.error('Error in POST /api/chat/conversations:', error);
    return Response.json({
      error: 'Internal server error',
      message: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}
import { NextRequest } from 'next/server';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { SignJWT } from 'jose';

export async function GET(request: NextRequest) {
  try {
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
        return Response.json({
          error: 'Unauthorized',
          hint: 'Please provide valid session cookie or Bearer token'
        }, { status: 401 });
      }

      token = authHeader.substring(7);

      // Verify the JWT token
      try {
        const verificationJWT = await auth.api.verifyJWT()

        userId = verificationJWT.payload?.sub;

        if (!userId) {
          return Response.json({
            error: 'User ID not found in token',
          }, { status: 401 });
        }

      } catch (error) {
        return Response.json({
          error: 'Invalid or expired token',
          message: error instanceof Error ? error.message : 'Unknown error'
        }, { status: 401 });
      }

    } else {
      // Session from cookies
      userId = session.session.userId;
    }

    if (!userId) {
      return Response.json({
        error: 'Invalid session data',
      }, { status: 401 });
    }

    // Mint a new JWT for the backend communication
    const secretValue = process.env.BETTER_AUTH_SECRET;
    if (!secretValue) {
      console.error("CRITICAL: BETTER_AUTH_SECRET is not set in environment variables!");
      return Response.json({ error: "Server misconfiguration" }, { status: 500 });
    }
    const secret = new TextEncoder().encode(secretValue);
    token = await new SignJWT({ sub: userId, user_id: userId }) // Include both to be safe
      .setProtectedHeader({ alg: 'HS256' })
      .setIssuedAt()
      .setExpirationTime('1m') // Short-lived token for internal call
      .sign(secret);

    // Call your FastAPI backend with the JWT token
    const backendUrl = process.env.BACKEND_API_URL || 'http://127.0.0.1:8000';
    const backendEndpoint = `${backendUrl}/api/${userId}/tasks`;

    const response = await fetch(backendEndpoint, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
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
    console.error('Error in GET /api/tasks:', error);
    return Response.json({
      error: 'Internal server error',
      message: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    // First try to get session from cookies (for browser)
    let session = await auth.api.getSession({
      headers: request.headers
    });

    let userId: string | undefined;
    let token: string | undefined;

    // If no session from cookies, try Bearer token
    if (!session?.session) {
      const authHeader = request.headers.get('Authorization');
      if (!authHeader?.startsWith('Bearer ')) {
        return Response.json({
          error: 'Unauthorized',
          hint: 'Please provide valid session cookie or Bearer token'
        }, { status: 401 });
      }

      token = authHeader.substring(7);

      // Verify the JWT token
      try {
        const verificationJWT = await auth.api.verifyJWT()

        userId = verificationJWT.payload?.sub;

        if (!userId) {
          return Response.json({
            error: 'User ID not found in token',
          }, { status: 401 });
        }

      } catch (error) {
        return Response.json({
          error: 'Invalid or expired token',
          message: error instanceof Error ? error.message : 'Unknown error'
        }, { status: 401 });
      }

    } else {
      // Session from cookies
      userId = session.session.userId;
    }

    if (!userId) {
      return Response.json({
        error: 'Invalid session data',
      }, { status: 401 });
    }

    // Mint a new JWT for the backend communication
    const secretValue = process.env.BETTER_AUTH_SECRET;
    if (!secretValue) {
      console.error("CRITICAL: BETTER_AUTH_SECRET is not set in environment variables!");
      return Response.json({ error: "Server misconfiguration" }, { status: 500 });
    }
    const secret = new TextEncoder().encode(secretValue);
    token = await new SignJWT({ sub: userId, user_id: userId })
      .setProtectedHeader({ alg: 'HS256' })
      .setIssuedAt()
      .setExpirationTime('1m')
      .sign(secret);

    const body = await request.json();

    // Call your FastAPI backend with the JWT token
    const backendUrl = process.env.BACKEND_API_URL || 'http://127.0.0.1:8000';
    const backendEndpoint = `${backendUrl}/api/${userId}/tasks`;

    const response = await fetch(backendEndpoint, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
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
    console.error('Error in POST /api/tasks:', error);
    return Response.json({
      error: 'Internal server error',
      message: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}
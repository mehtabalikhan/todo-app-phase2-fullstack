import { NextRequest } from 'next/server';
import { getServerSession } from 'next-auth/next';
import { authOptions } from '../../auth/[...nextauth]/route';

export async function GET(request: NextRequest) {
  return await handleRequest(request, 'GET');
}

export async function POST(request: NextRequest) {
  return await handleRequest(request, 'POST');
}

export async function PUT(request: NextRequest) {
  return await handleRequest(request, 'PUT');
}

export async function DELETE(request: NextRequest) {
  return await handleRequest(request, 'DELETE');
}

export async function PATCH(request: NextRequest) {
  return await handleRequest(request, 'PATCH');
}

async function handleRequest(request: NextRequest, method: string) {
  // Get the session server-side
  const session = await getServerSession(authOptions);

  if (!session) {
    return new Response(JSON.stringify({ error: 'Unauthorized' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Get user ID from session
  const userId = session.user?.id;
  if (!userId) {
    return new Response(JSON.stringify({ error: 'User ID not found in session' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Extract the path parts after /api/proxy
  const url = new URL(request.url);
  const pathParts = url.pathname.split('/api/proxy/')[1];
  if (!pathParts) {
    return new Response(JSON.stringify({ error: 'Invalid path' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Construct the backend API URL
  const backendBaseUrl = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
  const backendUrl = `${backendBaseUrl}/api/${userId}/${pathParts}`;

  try {
    // Forward the request to the backend
    const body = method !== 'GET' && method !== 'HEAD' ? await request.text() : undefined;

    const response = await fetch(backendUrl, {
      method,
      headers: {
        'Authorization': `Bearer ${session.accessToken}`,
        'Content-Type': 'application/json',
      },
      body,
    });

    // Forward the response from the backend
    const data = await response.json();
    return new Response(JSON.stringify(data), {
      status: response.status,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error('Proxy error:', error);
    return new Response(JSON.stringify({ error: 'Proxy request failed' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
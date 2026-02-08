import { NextApiHandler } from 'next';
import { unstable_getServerSession } from 'next-auth/next';
import { authOptions } from '../auth/[...nextauth]/route';

const proxyHandler: NextApiHandler = async (req, res) => {
  // Get the session server-side
  const session = await unstable_getServerSession(
    { req: { headers: req.headers, cookies: req.cookies } },
    { res: { getHeader: res.getHeader, setHeader: res.setHeader, statusCode: res.statusCode } },
    authOptions
  );

  if (!session) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  // Get user ID from session
  const userId = session.user?.id;
  if (!userId) {
    return res.status(401).json({ error: 'User ID not found in session' });
  }

  // Construct the backend API URL
  const backendBaseUrl = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
  const backendUrl = `${backendBaseUrl}/api/${userId}${req.url?.replace('/api/proxy', '')}`;

  try {
    // Forward the request to the backend
    const response = await fetch(backendUrl, {
      method: req.method,
      headers: {
        'Authorization': `Bearer ${session.accessToken}`,
        'Content-Type': 'application/json',
        ...req.headers,
      },
      body: req.body ? JSON.stringify(req.body) : undefined,
    });

    // Forward the response from the backend
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (error) {
    console.error('Proxy error:', error);
    res.status(500).json({ error: 'Proxy request failed' });
  }
};

export default proxyHandler;
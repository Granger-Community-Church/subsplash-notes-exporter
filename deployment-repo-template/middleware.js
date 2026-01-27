export default async function middleware(request) {
  // Get auth credentials from environment variables
  const validUsername = process.env.AUTH_USERNAME
  const validPassword = process.env.AUTH_PASSWORD

  // If no credentials configured, allow access (with warning)
  if (!validUsername || !validPassword) {
    console.warn('WARNING: AUTH_USERNAME or AUTH_PASSWORD not set. Auth is disabled.')
    return fetch(request)
  }

  // Get authorization header
  const authHeader = request.headers.get('authorization')

  if (!authHeader || !authHeader.startsWith('Basic ')) {
    return new Response('Authentication required', {
      status: 401,
      headers: {
        'WWW-Authenticate': 'Basic realm="Subsplash Notes"',
      },
    })
  }

  // Decode and validate credentials using Web APIs (Edge Runtime compatible)
  const base64Credentials = authHeader.split(' ')[1]
  const credentials = atob(base64Credentials)
  const [username, password] = credentials.split(':')

  if (username !== validUsername || password !== validPassword) {
    return new Response('Invalid credentials', {
      status: 401,
      headers: {
        'WWW-Authenticate': 'Basic realm="Subsplash Notes"',
      },
    })
  }

  // Auth successful - fetch and return the original request
  return fetch(request)
}

export const config = {
  matcher: '/:path*',
}

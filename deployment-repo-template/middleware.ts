import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Get auth credentials from environment variables
  const validUsername = process.env.AUTH_USERNAME
  const validPassword = process.env.AUTH_PASSWORD

  // If no credentials configured, allow access (with warning)
  if (!validUsername || !validPassword) {
    console.warn('WARNING: AUTH_USERNAME or AUTH_PASSWORD not set. Auth is disabled.')
    return NextResponse.next()
  }

  // Get authorization header
  const authHeader = request.headers.get('authorization')

  if (!authHeader || !authHeader.startsWith('Basic ')) {
    return new NextResponse('Authentication required', {
      status: 401,
      headers: {
        'WWW-Authenticate': 'Basic realm="Subsplash Notes"',
      },
    })
  }

  // Decode and validate credentials
  const base64Credentials = authHeader.split(' ')[1]
  const credentials = Buffer.from(base64Credentials, 'base64').toString('ascii')
  const [username, password] = credentials.split(':')

  if (username === validUsername && password === validPassword) {
    return NextResponse.next()
  }

  return new NextResponse('Invalid credentials', {
    status: 401,
    headers: {
      'WWW-Authenticate': 'Basic realm="Subsplash Notes"',
    },
  })
}

// Apply middleware to all routes
export const config = {
  matcher: '/:path*',
}

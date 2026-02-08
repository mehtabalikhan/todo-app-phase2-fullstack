'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  useEffect(() => {
    const checkAuth = () => {
      const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
      const currentUserEmail = localStorage.getItem('currentUserEmail');

      if (!isLoggedIn || !currentUserEmail) {
        console.log("Protected route accessed without authentication, redirecting to login");
        router.push('/login');
      }
    };

    checkAuth();
  }, [router]);

  return <>{children}</>;
}
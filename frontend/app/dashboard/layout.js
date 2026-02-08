'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function ProtectedLayout({ children }) {
  const router = useRouter();

  useEffect(() => {
    const checkAuth = () => {
      const userData = localStorage.getItem('user');
      const token = localStorage.getItem('accessToken');

      if (!userData || !token) {
        router.push('/signin');
      }
    };

    checkAuth();
  }, [router]);

  return <>{children}</>;
}
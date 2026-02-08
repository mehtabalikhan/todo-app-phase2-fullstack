'use client';

import { useState, useEffect } from 'react';
import { useSession } from 'next-auth/react';
import ProfileForm from '@/components/profile/profile-form';
import PreferencesForm from '@/components/profile/preferences-form';
import { User, UserPreferences } from '@/lib/types';

export default function ProfilePage() {
  const { data: session } = useSession();
  const [user, setUser] = useState<User | null>(null);
  const [preferences, setPreferences] = useState<UserPreferences | null>(null);
  const [activeTab, setActiveTab] = useState<'profile' | 'preferences'>('profile');

  useEffect(() => {
    if (session?.user) {
      // In a real app, we would fetch this from an API
      // For now, we'll create a mock user based on the session
      const mockUser: User = {
        id: session.user.id || 'mock-id',
        email: session.user.email || 'user@example.com',
        name: session.user.name || 'Mock User',
        createdAt: new Date(),
        updatedAt: new Date(),
        preferences: {
          theme: 'system',
          notificationsEnabled: true,
          taskSortOrder: 'createdAt',
          dateFormat: 'MM/DD/YYYY',
        }
      };
      setUser(mockUser);
      setPreferences(mockUser.preferences);
    }
  }, [session]);

  const handleProfileUpdate = async (formData: any) => {
    if (!user) return;

    // In a real app, this would update via API
    const updatedUser = { ...user, ...formData, updatedAt: new Date() };
    setUser(updatedUser);
    alert('Profile updated successfully!');
  };

  const handlePreferencesUpdate = async (formData: any) => {
    if (!user || !preferences) return;

    // In a real app, this would update via API
    const updatedPreferences = { ...preferences, ...formData };
    setPreferences(updatedPreferences);

    // Update user object as well
    setUser({ ...user, preferences: updatedPreferences });
    alert('Preferences updated successfully!');
  };

  if (!user) {
    return (
      <div className="flex justify-center items-center h-64">
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Profile Settings</h1>

      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('profile')}
            className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'profile'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Profile
          </button>
          <button
            onClick={() => setActiveTab('preferences')}
            className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'preferences'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Preferences
          </button>
        </nav>
      </div>

      <div className="mt-6">
        {activeTab === 'profile' && (
          <ProfileForm
            initialData={user}
            onSubmit={handleProfileUpdate}
          />
        )}

        {activeTab === 'preferences' && preferences && (
          <PreferencesForm
            initialData={preferences}
            onSubmit={handlePreferencesUpdate}
          />
        )}
      </div>
    </div>
  );
}
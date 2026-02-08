'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { UserPreferences } from '@/lib/types';

// Define the validation schema
const preferencesSchema = z.object({
  theme: z.enum(['light', 'dark', 'system']),
  notificationsEnabled: z.boolean(),
  taskSortOrder: z.enum(['dueDate', 'priority', 'createdAt']),
  dateFormat: z.string(),
  weeklyDigest: z.boolean().optional(),
});

type PreferencesFormData = z.infer<typeof preferencesSchema>;

interface PreferencesFormProps {
  initialData: UserPreferences;
  onSubmit: (data: PreferencesFormData) => void;
  onCancel?: () => void;
  loading?: boolean;
}

export default function PreferencesForm({ initialData, onSubmit, onCancel, loading }: PreferencesFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<PreferencesFormData>({
    resolver: zodResolver(preferencesSchema),
    defaultValues: {
      theme: initialData.theme,
      notificationsEnabled: initialData.notificationsEnabled,
      taskSortOrder: initialData.taskSortOrder,
      dateFormat: initialData.dateFormat,
      weeklyDigest: initialData.weeklyDigest ?? false,
    },
  });

  // Watch specific fields to conditionally render sections
  const notificationsEnabled = watch('notificationsEnabled');

  return (
    <Card>
      <CardHeader>
        <CardTitle>Preferences</CardTitle>
      </CardHeader>
      <form onSubmit={handleSubmit(onSubmit)}>
        <CardContent className="space-y-6">
          <div>
            <h3 className="text-lg font-medium mb-3">Appearance</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label htmlFor="theme" className="text-sm font-medium text-gray-700">
                  Theme
                </label>
                <select
                  id="theme"
                  {...register('theme')}
                  className="border border-input bg-background rounded-md px-3 py-2 text-sm"
                >
                  <option value="light">Light</option>
                  <option value="dark">Dark</option>
                  <option value="system">System</option>
                </select>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-medium mb-3">Notifications</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label htmlFor="notificationsEnabled" className="text-sm font-medium text-gray-700">
                  Enable Notifications
                </label>
                <input
                  id="notificationsEnabled"
                  type="checkbox"
                  {...register('notificationsEnabled')}
                  className="h-5 w-5 text-blue-600 rounded"
                />
              </div>

              {notificationsEnabled && (
                <div className="ml-6 space-y-2">
                  <div className="flex items-center justify-between">
                    <label htmlFor="weeklyDigest" className="text-sm font-medium text-gray-700">
                      Weekly Digest
                    </label>
                    <input
                      id="weeklyDigest"
                      type="checkbox"
                      {...register('weeklyDigest')}
                      className="h-5 w-5 text-blue-600 rounded"
                    />
                  </div>
                </div>
              )}
            </div>
          </div>

          <div>
            <h3 className="text-lg font-medium mb-3">Task Management</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label htmlFor="taskSortOrder" className="text-sm font-medium text-gray-700">
                  Default Sort Order
                </label>
                <select
                  id="taskSortOrder"
                  {...register('taskSortOrder')}
                  className="border border-input bg-background rounded-md px-3 py-2 text-sm"
                >
                  <option value="dueDate">Due Date</option>
                  <option value="priority">Priority</option>
                  <option value="createdAt">Creation Date</option>
                </select>
              </div>

              <div className="flex items-center justify-between">
                <label htmlFor="dateFormat" className="text-sm font-medium text-gray-700">
                  Date Format
                </label>
                <input
                  id="dateFormat"
                  type="text"
                  {...register('dateFormat')}
                  className="border border-input bg-background rounded-md px-3 py-2 text-sm w-32"
                  placeholder="MM/DD/YYYY"
                />
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          {onCancel && (
            <Button type="button" variant="outline" onClick={onCancel}>
              Cancel
            </Button>
          )}
          <Button type="submit" disabled={loading}>
            {loading ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Saving...
              </span>
            ) : (
              'Save Preferences'
            )}
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
}
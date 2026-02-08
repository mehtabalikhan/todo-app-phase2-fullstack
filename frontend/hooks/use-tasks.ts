import { useState, useEffect } from 'react';
import { Task } from '@/lib/types';
import { taskAPI } from '@/lib/api';
import { useSession } from 'next-auth/react';

export const useTasks = () => {
  const { data: session, status } = useSession();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async () => {
    if (status !== 'authenticated' || !session?.user?.id || !session.accessToken) {
      setError('User not authenticated');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await taskAPI.getTasks(session.user.id as string, session.accessToken);
      setTasks(response.tasks || []);
    } catch (err) {
      console.error('Failed to fetch tasks', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  const addTask = async (taskData: Omit<Task, 'id'>) => {
    if (status !== 'authenticated' || !session?.user?.id || !session.accessToken) {
      throw new Error('User not authenticated');
    }

    try {
      setLoading(true);
      const response = await taskAPI.createTask(session.user.id as string, session.accessToken, taskData);
      setTasks(prev => [...prev, response.task]);
      return response;
    } catch (err) {
      console.error('Failed to add task', err);
      setError(err instanceof Error ? err.message : 'Failed to add task');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateTask = async (taskId: string, taskData: Partial<Task>) => {
    if (status !== 'authenticated' || !session?.user?.id || !session.accessToken) {
      throw new Error('User not authenticated');
    }

    try {
      setLoading(true);
      const response = await taskAPI.updateTask(session.user.id as string, session.accessToken, taskId, taskData);
      setTasks(prev => prev.map(t => t.id === taskId ? response.task : t));
      return response;
    } catch (err) {
      console.error('Failed to update task', err);
      setError(err instanceof Error ? err.message : 'Failed to update task');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteTask = async (taskId: string) => {
    if (status !== 'authenticated' || !session?.user?.id || !session.accessToken) {
      throw new Error('User not authenticated');
    }

    try {
      setLoading(true);
      await taskAPI.deleteTask(session.user.id as string, session.accessToken, taskId);
      setTasks(prev => prev.filter(t => t.id !== taskId));
    } catch (err) {
      console.error('Failed to delete task', err);
      setError(err instanceof Error ? err.message : 'Failed to delete task');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const toggleTaskCompletion = async (taskId: string) => {
    if (status !== 'authenticated' || !session?.user?.id || !session.accessToken) {
      throw new Error('User not authenticated');
    }

    try {
      setLoading(true);
      const response = await taskAPI.toggleTaskCompletion(session.user.id as string, session.accessToken, taskId);
      setTasks(prev => prev.map(t => t.id === taskId ? response.task : t));
      return response;
    } catch (err) {
      console.error('Failed to toggle task completion', err);
      setError(err instanceof Error ? err.message : 'Failed to toggle task completion');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Fetch tasks when the hook mounts and when session changes
  useEffect(() => {
    if (status === 'authenticated') {
      fetchTasks();
    } else if (status === 'unauthenticated') {
      setTasks([]);
      setLoading(false);
    }
  }, [status]);

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    addTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  };
};
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function DashboardPage() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState(null);
  const router = useRouter();

  // Check if user is logged in
  useEffect(() => {
    const userData = localStorage.getItem('user');
    const token = localStorage.getItem('accessToken');

    if (!userData || !token) {
      router.push('/signin');
      return;
    }

    setUser(JSON.parse(userData));

    // Load todos from localStorage or fetch from backend
    loadTodos();
  }, []);

  const loadTodos = async () => {
    try {
      const token = localStorage.getItem('accessToken');
      const userData = JSON.parse(localStorage.getItem('user'));

      // Try to fetch from backend first
      const response = await fetch(`http://localhost:8000/api/${userData.email.split('@')[0]}s/tasks`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setTodos(data.tasks || []);
      } else {
        // Fallback to localStorage if backend fails
        const savedTodos = localStorage.getItem('todos');
        if (savedTodos) {
          setTodos(JSON.parse(savedTodos));
        } else {
          setTodos([]);
        }
      }
    } catch (error) {
      console.error('Error loading todos:', error);
      const savedTodos = localStorage.getItem('todos');
      if (savedTodos) {
        setTodos(JSON.parse(savedTodos));
      } else {
        setTodos([]);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const addTodo = async (e) => {
    e.preventDefault();
    if (!newTodo.trim()) return;

    try {
      const token = localStorage.getItem('accessToken');
      const userData = JSON.parse(localStorage.getItem('user'));

      // Try to add to backend first
      const response = await fetch(`http://localhost:8000/api/${userData.email.split('@')[0]}s/tasks`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: newTodo,
          description: newTodo,
          status: 'pending'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setTodos(prev => [...prev, data]);
      } else {
        // Fallback to localStorage
        const newTodoItem = {
          id: Date.now().toString(),
          title: newTodo,
          description: newTodo,
          status: 'pending',
          createdAt: new Date().toISOString(),
        };
        setTodos(prev => [...prev, newTodoItem]);
      }

      setNewTodo('');
    } catch (error) {
      console.error('Error adding todo:', error);
      // Fallback to localStorage
      const newTodoItem = {
        id: Date.now().toString(),
        title: newTodo,
        description: newTodo,
        status: 'pending',
        createdAt: new Date().toISOString(),
      };
      setTodos(prev => [...prev, newTodoItem]);
      setNewTodo('');
    }
  };

  const toggleTodo = async (todoId) => {
    try {
      const token = localStorage.getItem('accessToken');
      const userData = JSON.parse(localStorage.getItem('user'));

      // Try to update backend first
      const response = await fetch(`http://localhost:8000/api/${userData.email.split('@')[0]}s/tasks/${todoId}/complete`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const updatedTodos = todos.map(todo =>
          todo.id === todoId ? { ...todo, status: todo.status === 'completed' ? 'pending' : 'completed' } : todo
        );
        setTodos(updatedTodos);
      } else {
        // Fallback to localStorage
        const updatedTodos = todos.map(todo =>
          todo.id === todoId ? { ...todo, status: todo.status === 'completed' ? 'pending' : 'completed' } : todo
        );
        setTodos(updatedTodos);
      }
    } catch (error) {
      console.error('Error toggling todo:', error);
      // Fallback to localStorage
      const updatedTodos = todos.map(todo =>
        todo.id === todoId ? { ...todo, status: todo.status === 'completed' ? 'pending' : 'completed' } : todo
      );
      setTodos(updatedTodos);
    }
  };

  const deleteTodo = async (todoId) => {
    try {
      const token = localStorage.getItem('accessToken');
      const userData = JSON.parse(localStorage.getItem('user'));

      // Try to delete from backend first
      const response = await fetch(`http://localhost:8000/api/${userData.email.split('@')[0]}s/tasks/${todoId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        setTodos(prev => prev.filter(todo => todo.id !== todoId));
      } else {
        // Fallback to localStorage
        setTodos(prev => prev.filter(todo => todo.id !== todoId));
      }
    } catch (error) {
      console.error('Error deleting todo:', error);
      // Fallback to localStorage
      setTodos(prev => prev.filter(todo => todo.id !== todoId));
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('accessToken');
    router.push('/signin');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">Todo Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">Welcome, {user?.email}</span>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Add Todo Form */}
        <div className="bg-white shadow sm:rounded-lg mb-8">
          <div className="px-4 py-5 sm:p-6">
            <form onSubmit={addTodo} className="flex gap-3">
              <input
                type="text"
                value={newTodo}
                onChange={(e) => setNewTodo(e.target.value)}
                placeholder="Add a new task..."
                className="flex-1 min-w-0 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
              <button
                type="submit"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Add
              </button>
            </form>
          </div>
        </div>

        {/* Todo List */}
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <ul className="divide-y divide-gray-200">
            {todos.length === 0 ? (
              <li className="px-4 py-6 sm:px-6">
                <div className="text-center">
                  <p className="text-gray-500">No tasks yet. Add one above!</p>
                </div>
              </li>
            ) : (
              todos.map((todo) => (
                <li key={todo.id} className="px-4 py-4 sm:px-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        checked={todo.status === 'completed'}
                        onChange={() => toggleTodo(todo.id)}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <span
                        className={`ml-3 text-sm ${todo.status === 'completed' ? 'line-through text-gray-500' : 'text-gray-900'}`}
                      >
                        {todo.title}
                      </span>
                    </div>
                    <button
                      onClick={() => deleteTodo(todo.id)}
                      className="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                    >
                      Delete
                    </button>
                  </div>
                  {todo.description && todo.description !== todo.title && (
                    <p className="ml-7 mt-1 text-sm text-gray-500">{todo.description}</p>
                  )}
                  <p className="ml-7 mt-1 text-xs text-gray-400">
                    {new Date(todo.createdAt).toLocaleString()}
                  </p>
                </li>
              ))
            )}
          </ul>
        </div>
      </main>
    </div>
  );
}
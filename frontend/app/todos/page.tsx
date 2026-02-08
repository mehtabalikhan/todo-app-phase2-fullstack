'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function TodosPage() {
  const [todos, setTodos] = useState<{ id: string; text: string; completed: boolean }[]>([]);
  const [newTodo, setNewTodo] = useState('');
  const [currentUserEmail, setCurrentUserEmail] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    console.log("Checking authentication status...");

    // Check if user is logged in
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    const email = localStorage.getItem('currentUserEmail');

    if (!isLoggedIn || !email) {
      console.log("Not authenticated, redirecting to login");
      router.push('/login');
      return;
    }

    console.log("User is authenticated:", email);
    setCurrentUserEmail(email);

    // Load todos from localStorage
    try {
      const todosKey = `todos_${email}`;
      const storedTodos = localStorage.getItem(todosKey);
      if (storedTodos) {
        setTodos(JSON.parse(storedTodos));
        console.log("Loaded todos from localStorage:", JSON.parse(storedTodos));
      }
    } catch (error) {
      console.error("Error loading todos:", error);
      setTodos([]);
    }
  }, [router]);

  const addTodo = () => {
    if (!newTodo.trim() || !currentUserEmail) return;

    const newTodoItem = {
      id: Date.now().toString(),
      text: newTodo.trim(),
      completed: false,
    };

    const updatedTodos = [...todos, newTodoItem];
    setTodos(updatedTodos);

    // Save to localStorage
    try {
      const todosKey = `todos_${currentUserEmail}`;
      localStorage.setItem(todosKey, JSON.stringify(updatedTodos));
      console.log("Saved todo to localStorage:", newTodoItem);
    } catch (error) {
      console.error("Error saving todo:", error);
    }

    setNewTodo('');
  };

  const toggleTodo = (id: string) => {
    const updatedTodos = todos.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    );

    setTodos(updatedTodos);

    // Save to localStorage
    try {
      const todosKey = `todos_${currentUserEmail}`;
      localStorage.setItem(todosKey, JSON.stringify(updatedTodos));
      console.log("Updated todo completion in localStorage:", id);
    } catch (error) {
      console.error("Error saving todo update:", error);
    }
  };

  const deleteTodo = (id: string) => {
    const updatedTodos = todos.filter(todo => todo.id !== id);
    setTodos(updatedTodos);

    // Save to localStorage
    try {
      const todosKey = `todos_${currentUserEmail}`;
      localStorage.setItem(todosKey, JSON.stringify(updatedTodos));
      console.log("Deleted todo from localStorage:", id);
    } catch (error) {
      console.error("Error saving todo deletion:", error);
    }
  };

  const handleLogout = () => {
    console.log("Logging out user");
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('currentUserEmail');
    router.push('/login');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      addTodo();
    }
  };

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
              {currentUserEmail && (
                <span className="text-sm text-gray-600">Welcome, {currentUserEmail}</span>
              )}
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
            <div className="flex gap-3">
              <input
                type="text"
                value={newTodo}
                onChange={(e) => setNewTodo(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Add a new task..."
                className="flex-1 min-w-0 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
              <button
                onClick={addTodo}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Add
              </button>
            </div>
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
                        checked={todo.completed}
                        onChange={() => toggleTodo(todo.id)}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <span
                        className={`ml-3 text-sm ${todo.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}
                      >
                        {todo.text}
                      </span>
                    </div>
                    <button
                      onClick={() => deleteTodo(todo.id)}
                      className="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                    >
                      Delete
                    </button>
                  </div>
                </li>
              ))
            )}
          </ul>
        </div>
      </main>
    </div>
  );
}
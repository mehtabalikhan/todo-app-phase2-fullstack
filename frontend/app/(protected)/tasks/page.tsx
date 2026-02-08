'use client';

import { useState } from 'react';
import { useSession } from 'next-auth/react';
import TaskList from '@/components/tasks/task-list';
import TaskForm from '@/components/tasks/task-form';
import FilterBar from '@/components/tasks/filter-bar';
import { Button } from '@/components/ui/button';
import { Task, FilterState } from '@/lib/types';
import { useTasks } from '@/hooks/use-tasks';

export default function TasksPage() {
  const { data: session, status } = useSession();
  const {
    tasks,
    loading,
    error,
    addTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
    fetchTasks
  } = useTasks();

  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [filters, setFilters] = useState<FilterState>({
    status: 'all',
    priority: 'all',
    searchTerm: null,
  });

  const handleCreateTask = async (formData: any) => {
    if (status !== 'authenticated') return;

    try {
      const newTaskData = {
        title: formData.title,
        description: formData.description || null,
        priority: formData.priority || 'medium',
        dueDate: formData.dueDate || null,
      };

      await addTask(newTaskData);
      setShowForm(false);
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  const handleUpdateTask = async (formData: any) => {
    if (status !== 'authenticated' || !editingTask) return;

    try {
      const updatedTaskData = {
        title: formData.title,
        description: formData.description || null,
        priority: formData.priority || 'medium',
        dueDate: formData.dueDate || null,
      };

      await updateTask(editingTask.id, updatedTaskData);
      setEditingTask(null);
      setShowForm(false);
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const handleToggleComplete = async (taskId: string) => {
    if (status !== 'authenticated') return;

    try {
      await toggleTaskCompletion(taskId);
    } catch (error) {
      console.error('Error toggling task completion:', error);
    }
  };

  const handleDelete = async (taskId: string) => {
    if (status !== 'authenticated') return;

    try {
      await deleteTask(taskId);
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  const handleEdit = (task: Task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleFilterChange = (newFilters: FilterState) => {
    setFilters(newFilters);
  };

  const handleClearFilters = () => {
    setFilters({
      status: 'all',
      priority: 'all',
      searchTerm: null,
    });
  };

  // Apply filters to tasks
  const filteredTasks = tasks.filter(task => {
    // Apply status filter
    if (filters.status !== 'all') {
      if (filters.status === 'active' && task.completed) return false;
      if (filters.status === 'completed' && !task.completed) return false;
    }

    // Apply priority filter
    if (filters.priority !== 'all' && task.priority !== filters.priority) {
      return false;
    }

    // Apply search filter
    if (filters.searchTerm) {
      const lowerSearch = filters.searchTerm.toLowerCase();
      if (!task.title.toLowerCase().includes(lowerSearch) &&
          !(task.description && task.description.toLowerCase().includes(lowerSearch))) {
        return false;
      }
    }

    return true;
  });

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Tasks</h1>
        <Button onClick={() => { setShowForm(true); setEditingTask(null); }}>
          Add New Task
        </Button>
      </div>

      <FilterBar
        filters={filters}
        onFilterChange={handleFilterChange}
        onClearFilters={handleClearFilters}
      />

      {showForm ? (
        <div className="mb-6">
          <TaskForm
            onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
            onCancel={() => {
              setShowForm(false);
              setEditingTask(null);
            }}
            initialData={editingTask}
          />
        </div>
      ) : (
        <Button
          variant="outline"
          onClick={() => setShowForm(true)}
          className="mb-4"
        >
          + Add Task
        </Button>
      )}

      <TaskList
        tasks={filteredTasks}
        loading={loading}
        onToggleComplete={handleToggleComplete}
        onDelete={handleDelete}
        onEdit={handleEdit}
      />
    </div>
  );
}
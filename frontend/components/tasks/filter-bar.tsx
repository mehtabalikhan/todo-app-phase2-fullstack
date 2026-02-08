import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { FilterState } from '@/lib/types';

interface FilterBarProps {
  filters: FilterState;
  onFilterChange: (filters: FilterState) => void;
  onClearFilters: () => void;
}

const FilterBar: React.FC<FilterBarProps> = ({ filters, onFilterChange, onClearFilters }) => {
  const [searchTerm, setSearchTerm] = useState(filters.searchTerm || '');

  const handleStatusChange = (status: FilterState['status']) => {
    onFilterChange({ ...filters, status });
  };

  const handlePriorityChange = (priority: FilterState['priority']) => {
    onFilterChange({ ...filters, priority });
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchTerm(value);
    onFilterChange({ ...filters, searchTerm: value });
  };

  const isActive = (type: string, value: string) => {
    if (type === 'status') return filters.status === value;
    if (type === 'priority') return filters.priority === value;
    return false;
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-sm mb-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <div className="flex space-x-2">
            {(['all', 'active', 'completed'] as const).map((status) => (
              <Button
                key={status}
                variant={isActive('status', status) ? 'default' : 'outline'}
                size="sm"
                onClick={() => handleStatusChange(status)}
                className="capitalize"
              >
                {status}
              </Button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
          <div className="flex space-x-2">
            {(['all', 'low', 'medium', 'high'] as const).map((priority) => (
              <Button
                key={priority}
                variant={isActive('priority', priority) ? 'default' : 'outline'}
                size="sm"
                onClick={() => handlePriorityChange(priority)}
                className="capitalize"
              >
                {priority}
              </Button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
          <Input
            type="text"
            placeholder="Search tasks..."
            value={searchTerm}
            onChange={handleSearchChange}
            className="w-full"
          />
        </div>

        <div className="flex items-end">
          <Button
            variant="outline"
            onClick={onClearFilters}
            className="w-full"
          >
            Clear Filters
          </Button>
        </div>
      </div>
    </div>
  );
};

export default FilterBar;
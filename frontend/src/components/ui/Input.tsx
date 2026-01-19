import { InputHTMLAttributes } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export function Input({
  label,
  error,
  helperText,
  className = '',
  id,
  ...props
}: InputProps) {
  const errorOrHelper = error || helperText;
  const describedById = errorOrHelper ? `input-help-${Math.random().toString(36).substr(2, 9)}` : undefined;

  return (
    <div className="w-full">
      {label && (
        <label htmlFor={id} className="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
          {label}
        </label>
      )}
      <input
        id={id}
        className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition text-base ${
          error
            ? 'border-red-500 focus:ring-red-200 dark:focus:ring-red-900 focus:border-red-500 bg-red-50 dark:bg-red-900/20'
            : 'border-gray-300 dark:border-gray-600 focus:ring-blue-200 dark:focus:ring-blue-900 focus:border-blue-500 bg-white dark:bg-gray-700/50 text-gray-900 dark:text-white'
        } ${className}`}
        aria-invalid={!!error}
        aria-describedby={describedById}
        {...props}
      />
      {errorOrHelper && (
        <p id={describedById} className={`mt-2 text-sm ${error ? 'text-red-600 dark:text-red-400' : 'text-gray-500 dark:text-gray-400'}`}>
          {errorOrHelper}
        </p>
      )}
    </div>
  );
}
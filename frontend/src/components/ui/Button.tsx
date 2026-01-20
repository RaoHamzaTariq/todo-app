import { ButtonHTMLAttributes, ReactNode, ElementType } from 'react';
import { cn } from '../../lib/utils';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  asChild?: boolean;
  as?: ElementType;
}

export function Button({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  className = '',
  disabled,
  asChild = false,
  as,
  ...props
}: ButtonProps) {
  const baseClasses = 'inline-flex items-center justify-center rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap';

  const variantClasses = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white focus:ring-blue-500 border border-transparent',
    secondary: 'bg-gray-100 hover:bg-gray-200 text-gray-800 focus:ring-gray-500 border border-transparent',
    danger: 'bg-red-600 hover:bg-red-700 text-white focus:ring-red-500 border border-transparent',
    ghost: 'bg-transparent hover:bg-gray-100 text-gray-700 hover:text-gray-900 focus:ring-gray-500 border border-transparent',
    outline: 'bg-white hover:bg-gray-50 text-gray-700 border border-gray-300 hover:border-gray-400 focus:ring-gray-500 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700',
  };

  const sizeClasses = {
    sm: 'text-sm px-3 py-1.5',
    md: 'text-sm px-4 py-2',
    lg: 'text-base px-6 py-3',
  };

  const classes = cn(baseClasses, variantClasses[variant], sizeClasses[size], className);

  const Element = as || 'button';

  if (asChild) {
    return (
      <Element
        className={classes}
        disabled={disabled || loading}
        aria-busy={loading}
        {...(props as any)}
      >
        {loading ? (
          <span className="flex items-center">
            Loading...
          </span>
        ) : children}
      </Element>
    );
  }

  return (
    <Element
      className={classes}
      disabled={disabled || loading}
      aria-busy={loading}
      {...(props as any)}
    >
      {loading ? (
        <span className="flex items-center">
          Loading...
        </span>
      ) : children}
    </Element>
  );
}
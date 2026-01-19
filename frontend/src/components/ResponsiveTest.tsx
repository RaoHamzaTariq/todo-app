import { ReactNode } from 'react';

interface ResponsiveTestProps {
  children: ReactNode;
}

export default function ResponsiveTest({ children }: ResponsiveTestProps) {
  return (
    <div className="w-full">
      {/* Screen size indicators - visible only for testing */}
      <div className="fixed top-4 right-4 z-50 flex flex-col gap-1 text-xs font-mono bg-black/80 text-white p-2 rounded-md">
        <div className="hidden sm:block lg:hidden xl:hidden 2xl:hidden">SM</div>
        <div className="hidden md:block lg:hidden xl:hidden 2xl:hidden">MD</div>
        <div className="hidden lg:block xl:hidden 2xl:hidden">LG</div>
        <div className="hidden xl:block 2xl:hidden">XL</div>
        <div className="hidden 2xl:block">2XL</div>
      </div>

      {children}
    </div>
  );
}
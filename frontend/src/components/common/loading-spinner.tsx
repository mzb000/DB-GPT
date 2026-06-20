export function LoadingSpinner({ className = "h-8 w-8" }: { className?: string }) {
  return (
    <div className="flex items-center justify-center">
      <div className={`animate-spin rounded-full border-4 border-primary border-t-transparent ${className}`} />
    </div>
  );
}

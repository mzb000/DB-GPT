import { Card, CardContent, CardHeader } from "@/components/ui/card";

export function SkeletonTable({ rows = 5 }: { rows?: number }) {
  return (
    <Card>
      <CardHeader className="pb-2">
        <div className="h-5 w-32 animate-pulse rounded bg-muted" />
      </CardHeader>
      <CardContent>
        <div className="space-y-1">
          <div className="flex gap-4 border-b pb-3">
            <div className="h-4 w-1/3 animate-pulse rounded bg-muted" />
            <div className="h-4 w-1/6 animate-pulse rounded bg-muted" />
            <div className="h-4 w-1/4 animate-pulse rounded bg-muted" />
            <div className="h-4 w-1/6 animate-pulse rounded bg-muted" />
          </div>
          {Array.from({ length: rows }).map((_, i) => (
            <div key={i} className="flex gap-4 border-b py-3 last:border-0">
              <div className="h-4 w-1/3 animate-pulse rounded bg-muted" style={{ opacity: 1 - i * 0.1 }} />
              <div className="h-4 w-1/6 animate-pulse rounded bg-muted" style={{ opacity: 1 - i * 0.1 }} />
              <div className="h-4 w-1/4 animate-pulse rounded bg-muted" style={{ opacity: 1 - i * 0.1 }} />
              <div className="h-4 w-1/6 animate-pulse rounded bg-muted" style={{ opacity: 1 - i * 0.1 }} />
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

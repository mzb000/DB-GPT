import { Card, CardContent } from "@/components/ui/card";

interface Props {
  icon?: React.ReactNode;
  title: string;
  description?: string;
}

export function EmptyState({ icon, title, description }: Props) {
  return (
    <Card>
      <CardContent className="flex flex-col items-center gap-4 py-20">
        {icon}
        <p className="text-muted-foreground">{title}</p>
        {description && <p className="text-sm text-muted-foreground">{description}</p>}
      </CardContent>
    </Card>
  );
}

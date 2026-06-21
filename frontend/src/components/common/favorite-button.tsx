"use client";

import { Star } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface FavoriteButtonProps {
  favorited: boolean;
  onToggle: () => void;
  className?: string;
}

export function FavoriteButton({ favorited, onToggle, className }: FavoriteButtonProps) {
  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={(e) => { e.preventDefault(); e.stopPropagation(); onToggle(); }}
      className={cn("h-8 w-8", className)}
    >
      <Star
        className={cn(
          "h-4 w-4 transition-colors",
          favorited ? "fill-yellow-400 text-yellow-400" : "text-muted-foreground"
        )}
      />
    </Button>
  );
}

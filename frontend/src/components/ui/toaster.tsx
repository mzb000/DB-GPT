"use client";

import { useToast } from "@/hooks/use-toast";
import {
  Toast,
  ToastClose,
  ToastDescription,
  ToastProvider,
  ToastTitle,
  ToastViewport,
} from "@/components/ui/toast";
import { CheckCircle2, AlertCircle, Info } from "lucide-react";

const variantIcon: Record<string, React.ReactNode> = {
  default: <Info className="h-4 w-4 text-blue-500" />,
  destructive: <AlertCircle className="h-4 w-4" />,
  success: <CheckCircle2 className="h-4 w-4 text-green-500" />,
};

export function Toaster() {
  const { toasts } = useToast();

  return (
    <ToastProvider>
      {toasts.map(function ({ id, title, description, action, ...props }) {
        const icon = variantIcon[(props.variant as string) || "default"];
        return (
          <Toast key={id} {...props}>
            <div className="flex items-start gap-3">
              {icon && <div className="mt-0.5 shrink-0">{icon}</div>}
              <div className="grid gap-1">
                {title && <ToastTitle>{title}</ToastTitle>}
                {description && <ToastDescription>{description}</ToastDescription>}
              </div>
            </div>
            {action}
            <ToastClose />
          </Toast>
        );
      })}
      <ToastViewport />
    </ToastProvider>
  );
}

"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api-client";
import type { User } from "@/types";

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      api.get<User>("/api/v1/auth/me")
        .then(setUser)
        .catch(() => localStorage.removeItem("token"))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const res = await api.post<{ access_token: string }>("/api/v1/auth/login", { email, password });
    localStorage.setItem("token", res.access_token);
    const me = await api.get<User>("/api/v1/auth/me");
    setUser(me);
    router.push("/chat");
  }, [router]);

  const register = useCallback(async (email: string, password: string, fullName: string) => {
    const res = await api.post<{ access_token: string }>("/api/v1/auth/register", { email, password, full_name: fullName });
    localStorage.setItem("token", res.access_token);
    const me = await api.get<User>("/api/v1/auth/me");
    setUser(me);
    router.push("/chat");
  }, [router]);

  const logout = useCallback(() => {
    localStorage.removeItem("token");
    setUser(null);
    router.push("/login");
  }, [router]);

  return { user, loading, login, register, logout };
}

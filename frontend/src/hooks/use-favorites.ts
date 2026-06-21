"use client";

import { useState, useEffect, useCallback } from "react";
import { api } from "@/lib/api-client";

interface FavoriteItem {
  id: string;
  entity_type: string;
  entity_id: string;
}

export function useFavorites() {
  const [favorites, setFavorites] = useState<FavoriteItem[]>([]);

  useEffect(() => {
    api.get<FavoriteItem[]>("/api/v1/favorites/")
      .then(setFavorites)
      .catch(() => {});
  }, []);

  const isFavorited = useCallback(
    (type: string, id: string) => favorites.some((f) => f.entity_type === type && f.entity_id === id),
    [favorites]
  );

  const toggle = useCallback(async (type: string, id: string) => {
    const result = await api.post<{ favorited: boolean }>("/api/v1/favorites/", {
      entity_type: type,
      entity_id: id,
    });
    if (result.favorited) {
      setFavorites((prev) => [...prev, { id: "", entity_type: type, entity_id: id }]);
    } else {
      setFavorites((prev) => prev.filter((f) => !(f.entity_type === type && f.entity_id === id)));
    }
    return result.favorited;
  }, []);

  return { favorites, isFavorited, toggle };
}

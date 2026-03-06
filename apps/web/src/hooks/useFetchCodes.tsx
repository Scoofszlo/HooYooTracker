import type { APIResult } from "@hooyootracker/core";
import { useQuery } from "@tanstack/react-query";
import { getCodes } from "../services/local/service";
import type { Games } from "../types";

export type FetchedCodeContext = {
  result: APIResult | undefined;
  error: Error | null;
  refetch: () => void;
  isLoading: boolean;
  isRefetching: boolean;
};

export function useFetchCodes(selectedGame: Games) {
  const {
    data: gi,
    error: giError,
    refetch: giRefetch,
    isLoading: giisLoading,
    isRefetching: giIsRefetching,
  } = useQuery({
    queryKey: ["codes", "gi"],
    queryFn: () => getCodes("gi"),
    enabled: selectedGame === "Genshin Impact",
    retry: (failureCount) => {
      return failureCount < 0;
    },
  });

  const {
    data: zzz,
    error: zzzError,
    refetch: zzzRefetch,
    isLoading: zzzIsLoading,
    isRefetching: zzzIsRefetching,
  } = useQuery({
    queryKey: ["codes", "zzz"],
    queryFn: () => getCodes("zzz"),
    enabled: selectedGame === "Zenless Zone Zero",
    retry: (failureCount) => {
      return failureCount < 0;
    },
  });

  const refetch = () => {
    if (selectedGame === "Genshin Impact") {
      giRefetch();
    } else {
      zzzRefetch();
    }
  };

  return {
    gi: {
      result: gi,
      error: giError,
      isLoading: giisLoading,
      isRefetching: giIsRefetching,
      refetch: giRefetch,
    },
    zzz: {
      result: zzz,
      error: zzzError,
      isLoading: zzzIsLoading,
      isRefetching: zzzIsRefetching,
      refetch: zzzRefetch,
    },
    refetch,
  };
}

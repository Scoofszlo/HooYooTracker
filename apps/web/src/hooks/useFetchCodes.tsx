import type { APIResult } from "@hooyootracker/core";
import { useQuery } from "@tanstack/react-query";
import { GAME_CONFIG } from "../constants";
import { getCodes } from "../services/local/service";
import type { Games } from "../types";

export type FetchedCodeContext = {
  result: APIResult | undefined;
  error: Error | null;
};

type RefetchCallbacks = {
  onRefetch?: () => void;
  onSuccess?: () => void;
  onError?: () => void;
};

export function useFetchCodes(selectedGame: Games) {
  const selectedConfig = GAME_CONFIG[selectedGame];

  const {
    data,
    error,
    refetch: queryRefetch,
    isLoading,
    isRefetching,
  } = useQuery<APIResult, Error>({
    queryKey: ["codes", selectedConfig.query],
    queryFn: () => getCodes(selectedConfig.query),
    retry: 1,
  });

  const refetch = async ({
    onRefetch,
    onSuccess,
    onError,
  }: RefetchCallbacks) => {
    onRefetch?.();
    const refreshResult = await queryRefetch();

    if (refreshResult.error) {
      onError?.();
    } else {
      onSuccess?.();
    }
  };

  return {
    data,
    error,
    refetch,
    isLoading,
    isRefetching,
  };
}

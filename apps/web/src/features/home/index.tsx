import type { APIResult } from "@hooyootracker/core";
import RefreshIcon from "@mui/icons-material/Refresh";
import CircularProgress from "@mui/material/CircularProgress";
import clsx from "clsx";
import { useState } from "react";
import { Content } from "../../components/layout/Content";
import { Card } from "../../components/ui/Card";
import { FilterChip } from "../../components/ui/FilterChip";
import IconButton from "../../components/ui/IconButton";
import { Spacer } from "../../components/ui/Spacer";
import { GAME_CONFIG, GAME_LIST } from "../../constants";
import { useElapsedTime } from "../../hooks/useElapsedTime";
import { useFetchCodes } from "../../hooks/useFetchCodes";
import usePageTitle from "../../hooks/usePageTitle";
import { useSnackbarStore } from "../../state_management/store/useSnackbarStore";
import type { Games } from "../../types";
import { formatTimeAndDate } from "../../utils";

export function Home() {
  const [game, setGame] = useState<Games>("Genshin Impact");
  const { data, error, refetch, isLoading, isRefetching } = useFetchCodes(game);

  usePageTitle("Home");

  return (
    <Content className="p-4 lg:p-8">
      <div className="flex flex-col sm:flex-row gap-2 sm:gap-8 sm:justify-between sm:items-center">
        <div className="flex flex-col">
          <h1 className="text-2xl font-bold">List of Codes</h1>
          <Spacer size="0.5rem" />
          <Filters selectedFilter={game} onSelect={setGame} />
        </div>
        <RefreshButton onClick={() => refetch()} />
      </div>
      <Spacer size="2rem" />
      <CodeList
        data={data}
        error={error}
        game={game}
        isLoading={isLoading}
        isRefetching={isRefetching}
      />
    </Content>
  );
}

function CodeList({
  data,
  error,
  game,
  isLoading,
  isRefetching,
}: {
  data: APIResult | undefined;
  error: Error | null;
  game: Games;
  isLoading: boolean;
  isRefetching: boolean;
}) {
  const redeemBaseUrl = GAME_CONFIG[game].redeemBaseUrl;

  if (isLoading || isRefetching) {
    return (
      <div className="flex justify-center items-center h-32">
        <CircularProgress color="inherit" />
      </div>
    );
  }

  if (error) {
    return (
      <Card>
        <p>Error fetching codes</p>
      </Card>
    );
  }

  if (!data || data.codes.length === 0) {
    return (
      <Card>
        <p>No codes available for {game}.</p>
      </Card>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      <LastFetched date={data.date} />
      <div className="grid sm:grid-cols-2 gap-4">
        {data.codes.map((entry) => (
          <Card key={entry.code} className="gap-4">
            <div className="flex flex-col">
              <a
                className="text-xl font-bold hover:cursor-pointer hover:text-md-on-background/62 transition-all"
                href={`${redeemBaseUrl}${entry.code}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                {entry.code}
              </a>
              <p>{entry.description}</p>
            </div>
            <a
              className={clsx(
                "text-sm mt-auto hover:cursor-pointer text-md-on-surface-variant",
                "hover:text-md-on-surface-variant/62 transition-all",
              )}
              href={entry.source.url}
              target="_blank"
              rel="noopener noreferrer"
            >
              Source: {entry.source.name}
            </a>
          </Card>
        ))}
      </div>
    </div>
  );
}

function RefreshButton({ onClick }: { onClick: () => void }) {
  return (
    <div>
      <IconButton
        outlinedIcon={<RefreshIcon />}
        filledIcon={<RefreshIcon />}
        onClick={onClick}
      />
    </div>
  );
}

function Filters({
  selectedFilter,
  onSelect,
}: {
  selectedFilter: Games;
  onSelect: (filter: Games) => void;
}) {
  return (
    <div className="flex flex-row flex-wrap gap-2">
      {GAME_LIST.map((game) => (
        <FilterChip
          key={game}
          label={game}
          selected={selectedFilter === game}
          onClick={() => onSelect(game)}
        />
      ))}
    </div>
  );
}

function LastFetched({ date }: { date: string }) {
  const elapsed = useElapsedTime(date);

  return (
    <p className="text-sm text-md-on-surface-variant">
      Last refreshed: {elapsed} ago | {formatTimeAndDate(date)}
    </p>
  );
}

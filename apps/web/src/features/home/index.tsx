import CircularProgress from "@mui/material/CircularProgress";
import { useState } from "react";
import { Content } from "../../components/layout/Content";
import { Card } from "../../components/ui/Card";
import { FilterChip } from "../../components/ui/FilterChip";
import { Spacer } from "../../components/ui/Spacer";
import {
  useFetchCodes,
  type FetchedCodeContext,
} from "../../hooks/useFetchCodes";
import usePageTitle from "../../hooks/usePageTitle";
import type { Games } from "../../types";
import { formatTimeAndDate } from "../../utils";
import RefreshIcon from "@mui/icons-material/Refresh";
import IconButton from "../../components/ui/IconButton";
import { useElapsedTime } from "../../hooks/useElapsedTime";

export function Home() {
  const [game, setGame] = useState<Games>("Genshin Impact");
  const { gi, zzz, refetch } = useFetchCodes(game);

  usePageTitle("Home");

  return (
    <Content className="lg:mt-8 p-4">
      <div className="flex flex-col sm:flex-row gap-2 sm:gap-8 sm:justify-between sm:items-center">
        <div className="flex flex-col">
          <h1 className="text-2xl font-bold">List of Codes</h1>
          <Spacer size="0.5rem" />
          <Filters selectedFilter={game} onSelect={setGame} />
        </div>
        <RefreshButton onClick={() => refetch()} />
      </div>
      <Spacer size="2rem" />
      {game === "Genshin Impact" && <CodeList context={gi} game={game} />}
      {game === "Zenless Zone Zero" && <CodeList context={zzz} game={game} />}
    </Content>
  );
}

function CodeList({
  context,
  game,
}: {
  context: FetchedCodeContext;
  game: Games;
}) {
  const { result, error, isLoading, isRefetching } = context;
  const getLink = (code: string) => {
    if (game === "Genshin Impact") {
      return `https://genshin.hoyoverse.com/en/gift?code=${code}`;
    } else if (game === "Zenless Zone Zero") {
      return `https://zenless.hoyoverse.com/redemption?code=${code}`;
    }
  };

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

  if (!result || result.codes.length === 0) {
    return (
      <Card>
        <p>No codes available for {game}.</p>
      </Card>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      <LastFetched date={result.date} />
      <div className="grid sm:grid-cols-2 gap-4">
        {result.codes.map((res) => (
          <Card key={res.code}>
            <a
              className="text-xl font-bold hover:cursor-pointer hover:text-md-on-background/62 transition-all"
              href={getLink(res.code)}
              target="_blank"
              rel="noopener noreferrer"
            >
              {res.code}
            </a>
            <p>{res.description}</p>
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
      <FilterChip
        label="Genshin Impact"
        selected={selectedFilter === "Genshin Impact"}
        onClick={() => onSelect("Genshin Impact")}
      />
      <FilterChip
        label="Zenless Zone Zero"
        selected={selectedFilter === "Zenless Zone Zero"}
        onClick={() => onSelect("Zenless Zone Zero")}
      />
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

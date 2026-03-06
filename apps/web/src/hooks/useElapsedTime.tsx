import { useEffect, useState } from "react";
import { formatElapsed } from "../utils";

export function useElapsedTime(dateString: string | undefined): string {
  const [elapsed, setElapsed] = useState<string>("");

  useEffect(() => {
    if (!dateString) return;

    const update = () => {
      const diff = Date.now() - new Date(dateString).getTime();
      setElapsed(formatElapsed(diff));
    };

    update(); // run immediately
    const interval = setInterval(update, 1000);
    return () => clearInterval(interval);
  }, [dateString]);

  return elapsed;
}

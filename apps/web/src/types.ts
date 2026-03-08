import type { GAME_CONFIG } from "./constants";

export type Games = keyof typeof GAME_CONFIG;
export type GameQuery = (typeof GAME_CONFIG)[Games]["query"];

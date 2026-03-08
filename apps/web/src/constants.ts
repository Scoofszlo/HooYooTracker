export const APP = {
  NAME: "HooYooTracker",
};

export const GAME_CONFIG = {
  "Genshin Impact": {
    query: "gi",
    redeemBaseUrl: "https://genshin.hoyoverse.com/en/gift?code=",
  },
  "Zenless Zone Zero": {
    query: "zzz",
    redeemBaseUrl: "https://zenless.hoyoverse.com/redemption?code=",
  },
} as const;

export const GAME_LIST = Object.keys(GAME_CONFIG) as Array<keyof typeof GAME_CONFIG>;

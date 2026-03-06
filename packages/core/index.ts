export type Game = "Genshin Impact" | "Zenless Zone Zero";
export type RedeemCode = {
  code: string;
  description: string;
  source: string;
}
export type APIResult = {
  codes: RedeemCode[];
  date: string;
}

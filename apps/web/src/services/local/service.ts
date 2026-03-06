import type { APIResult } from "@hooyootracker/core";
import api from "./api";

export async function getCodes(gameQuery: string): Promise<APIResult> {
  const response = await api.get(`/api/codes?game=${gameQuery}`);
  
  return response.data;
} 

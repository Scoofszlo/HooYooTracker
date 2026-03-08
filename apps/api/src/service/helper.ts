import type { RedeemCode } from "@hooyootracker/core";

export async function getUniqueCodes(
  results: RedeemCode[],
): Promise<RedeemCode[]> {
  const uniqueMap = new Map<string, RedeemCode>();

  results.forEach((code) => {
    if (!uniqueMap.has(code.code)) {
      uniqueMap.set(code.code, code);
    }
  });

  return Array.from(uniqueMap.values());
}

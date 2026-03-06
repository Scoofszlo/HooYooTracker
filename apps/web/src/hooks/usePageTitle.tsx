import { useEffect } from "react";
import { APP } from "../constants";

export default function usePageTitle(title?: string, useTitleSuffix: boolean = true) {
  useEffect(() => {
    if (useTitleSuffix) {
      document.title = title ? `${title} | ${APP.NAME}` : APP.NAME;
    } else {
      document.title = title ? `${title}` : APP.NAME;
    }
    
  }, [title, useTitleSuffix]);
}

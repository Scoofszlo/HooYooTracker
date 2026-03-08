import { create } from "zustand";

type Status = "success" | "processing" | "error" | "info";

type SnackbarState = {
  message: string | null;
  open: boolean;
  status: Status;
  show: (message: string, status?: Status, duration?: number) => void;
  hide: () => void;
};

let timeout: ReturnType<typeof setTimeout> | null = null;

export const useSnackbarStore = create<SnackbarState>((set) => ({
  message: null,
  open: false,
  status: "info",

  show: (message, status, duration = 3000) => {
    if (timeout) clearTimeout(timeout);

    set({
      message,
      open: true,
      status: status || "info",
    });

    if (status !== "processing") {
      timeout = setTimeout(() => {
        set({
          open: false,
          message: null,
        });
      }, duration);
    }
  },

  hide: () =>
    set({
      open: false,
      message: null,
    }),
}));

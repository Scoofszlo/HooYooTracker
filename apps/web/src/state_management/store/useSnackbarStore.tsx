import { create } from "zustand";

type Status = "success" | "processing" | "error" | "info";

type SnackbarState = {
  message: string | null;
  open: boolean;
  status: Status;
  action?: Action;
  showDismiss?: boolean;
  show: (message: string, options?: SnackbarOptions) => void;
  hide: () => void;
};

type SnackbarOptions = {
  status?: Status;
  duration?: number;
  action?: Action;
  showDismiss?: boolean;
};

type Action = {
  name: string;
  handler: () => void;
}

const snackbarDefaultState = {
  message: null,
  open: false,
  status: "info" as Status,
  showDismiss: false,
};

let timeout: ReturnType<typeof setTimeout> | null = null;

export const useSnackbarStore = create<SnackbarState>((set) => ({
  message: null,
  open: false,
  status: "info",
  showDismiss: false,

  show: (message, options?: SnackbarOptions) => {
    if (timeout) clearTimeout(timeout);

    const status = options?.status ?? "info";
    const duration = options?.duration ?? 3000;
    const showDismiss = options?.showDismiss ?? false;
    const action = options?.action;

    set({
      message,
      open: true,
      status,
      showDismiss,
      action,
    });

    if (status !== "processing") {
      timeout = setTimeout(() => {
        set(snackbarDefaultState);
      }, duration);
    }
  },

  hide: () => {
    if (timeout) clearTimeout(timeout);
    set(snackbarDefaultState);
  },
}));

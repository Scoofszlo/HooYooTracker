import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ErrorIcon from "@mui/icons-material/Error";
import clsx from "clsx";
import { useSnackbarStore } from "../../../state_management/store/useSnackbarStore";

export function Snackbar() {
  const { message, open, status } = useSnackbarStore();

  if (!open) return null;

  return (
    <div
      className={clsx(
        "flex flex-row fixed items-center rounded-lg",
        "left-1/2 -translate-x-1/2 z-10 bottom-8 w-96 h-12 p-4 gap-4",
        "bg-md-inverse-surface text-md-inverse-on-surface rounded-lg",
        "shadow-md-shadow",
      )}
    >
      {status === "success" && (
        <div className="text-md-on-inverse-surface">
          <CheckCircleIcon />
        </div>
      )}
      {status === "processing" && (
        <div className="w-6">
          <Spinner />
        </div>
      )}
      {status === "error" && (
        <div className="text-md-on-inverse-surface">
          <ErrorIcon />
        </div>
      )}
      <p className="text-sm">{message}</p>
    </div>
  );
}

function Spinner() {
  return (
    <svg
      className={clsx(
        "animate-spin border-md-inverse-on-surface border-t-transparent",
        "rounded-full border-4",
      )}
      viewBox="0 0 24 24"
    ></svg>
  );
}

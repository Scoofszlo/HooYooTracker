import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import CloseIcon from "@mui/icons-material/Close";
import ErrorIcon from "@mui/icons-material/Error";
import clsx from "clsx";
import { useSnackbarStore } from "../../../state_management/store/useSnackbarStore";

export function Snackbar() {
  const { message, open, hide, status, showDismiss } = useSnackbarStore();

  if (!open) return null;

  return (
    <div
      className={clsx(
        "flex flex-row fixed items-center rounded-lg",
        "left-1/2 -translate-x-1/2 z-10 bottom-8 w-96 pt-3 pb-3 pl-4 pr-4 gap-4",
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
        <div className="w-6 min-w-6">
          <Spinner />
        </div>
      )}
      {status === "error" && (
        <div className="text-md-on-inverse-surface">
          <ErrorIcon />
        </div>
      )}
      <p className="text-sm text-wrap break-all">{message}</p>
      {showDismiss && <DismissButton onClick={hide} />}
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

function DismissButton({ onClick }: { onClick: () => void }) {
  return (
    <button
      className={clsx(
        "ml-auto text-sm text-md-inverse-on-surface min-w-fit",
        "cursor-pointer hover:text-md-inverse-on-surface/62 transition-all",
      )}
      onClick={onClick}
    >
      <CloseIcon />
    </button>
  );
}

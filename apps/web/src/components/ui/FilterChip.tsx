import clsx from "clsx";

type FilterChipProps = {
  label: string;
  icon?: React.ReactNode;
  selected?: boolean;
  disabled?: boolean;
  onClick?: () => void;
};

export function FilterChip({
  label,
  icon,
  selected,
  disabled,
  onClick,
}: FilterChipProps) {

  return (
    <button
      className={clsx(
        "flex justify-center gap-2 h-8 rounded-lg",
        "w-fit min-w-fit items-center ",
        !disabled && "hover:cursor-pointer",
        !disabled && selected && "bg-md-secondary-container border-md-secondary-container",
        !disabled && !selected && "bg-md-surface-container-low border-md-outline-variant border",
        disabled && "cursor-not-allowed bg-md-on-surface/12 border-md-on-surface/12 border",
        icon ? "pl-2 pr-4" : "pl-4 pr-4",
      )}
      onClick={onClick}
      disabled={disabled}
    >
      {icon && <div className="flex text-lg text-md-on-surface-variant">{icon}</div>}
      <p className={clsx(
        "leading-none -mt-0.5 text-nowrap",
        disabled && "text-md-on-surface/38"
      )}>{label}</p>
    </button>
  );
}

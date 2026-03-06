import clsx from "clsx";

type CardProps = {
  disabled?: boolean;
  children?: React.ReactNode;
};

export function Card({ disabled, children }: CardProps) {
  return (
    <div className={clsx(
      "bg-md-surface border-md-outline-variant border rounded-xl p-4",
      disabled && "border-md-outline/12 text-md-on-surface/38"
    )}>
      {children}
    </div>
  )
}

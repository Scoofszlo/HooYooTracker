import clsx from "clsx";

type CardProps = {
  disabled?: boolean;
  children?: React.ReactNode;
  className?: string;
};

export function Card({ disabled, children, className }: CardProps) {
  return (
    <div className={clsx(
      "flex flex-col bg-md-surface border-md-outline-variant border rounded-xl p-4",
      disabled && "border-md-outline/12 text-md-on-surface/38",
      className
    )}>
      {children}
    </div>
  )
}

import React, { useState } from "react";
import clsx from "clsx";

type IconButtonProps = {
  label?: string;
  outlinedIcon: React.ReactNode;
  filledIcon: React.ReactNode;
  disabled?: boolean;
  className?: string;
  onClick?: () => void;
};

export default function IconButton({
  label,
  outlinedIcon,
  filledIcon,
  disabled,
  onClick,
  className,
}: IconButtonProps) {
  const [hovered, setHovered] = useState(false);

  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      className={clsx(
        "flex items-center gap-2 p-2 justify-center rounded-full transition-colors duration-200",
        "text-md-on-surface-variant",
        "bg-transparent hover:bg-md-on-surface-variant/8",
        disabled
          ? "cursor-not-allowed opacity-38 hover:bg-transparent"
          : "cursor-pointer",
        className,
      )}
      style={{ aspectRatio: 1, minWidth: "40px", minHeight: "40px" }}
      disabled={disabled}
    >
      {hovered ? filledIcon : outlinedIcon}
      {label && <span>{label}</span>}
    </button>
  );
}

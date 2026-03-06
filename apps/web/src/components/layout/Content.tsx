type ContentProps = {
  noWidthRestriction?: boolean;
  className?: string;
  children?: React.ReactNode;
};

export function Content({
  noWidthRestriction = false,
  className,
  children,
}: ContentProps) {
  if (noWidthRestriction) {
    return <div className={className}>{children}</div>;
  }

  return (
    <div className={`w-full flex justify-center ${className || ''}`}>
      <div className="w-full max-w-5xl">{children}</div>
    </div>
  );
}

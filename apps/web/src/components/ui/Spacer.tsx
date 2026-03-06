export function Spacer({ size }: { size: string }) {
  return (
    <div
      style={{
        width: size,
        height: size,
        minWidth: size,
        minHeight: size,
        display: "block",
      }}
      aria-hidden="true"
    />
  );
}

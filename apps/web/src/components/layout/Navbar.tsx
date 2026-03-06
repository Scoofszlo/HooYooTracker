import { APP } from "../../constants";

type NavbarProps = {
  children?: React.ReactNode;
};

export default function Navbar({ children }: NavbarProps) {
  return (
    <div className="flex flex-row w-full justify-between items-center p-4 bg-md-surface-container text-md-on-primary fixed top-0 h-18">
      <p className="font-bold text-lg flex text-md-on-surface-variant">{APP.NAME}</p>
      <div className="flex flex-row items-center gap-1">{children}</div>
    </div>
  );
}

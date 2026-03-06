import DarkModeIcon from "@mui/icons-material/DarkMode";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";
import SettingsIcon from '@mui/icons-material/Settings';
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
import { Outlet } from "react-router";
import usePageTitle from "../../hooks/usePageTitle";
import { useTheme } from "../../provider/theme/hooks";
import IconButton from "../ui/IconButton";
import Navbar from "./Navbar";

export function GenericLayout() {
  const { toggleTheme } = useTheme();
  usePageTitle("Home");

  return (
    <div className="flex gap-4 flex-col mt-18">
      <Navbar>
        <IconButton
          outlinedIcon={<DarkModeOutlinedIcon />}
          filledIcon={<DarkModeIcon />}
          onClick={() => toggleTheme()}
        />
        <IconButton
          outlinedIcon={<SettingsOutlinedIcon />}
          filledIcon={<SettingsIcon />}
          disabled
        />
      </Navbar>
      <Outlet />
    </div>
  );
}

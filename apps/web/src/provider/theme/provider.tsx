import { useEffect, useState } from "react";
import { ThemeContext, type Theme } from "./constants";

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>(
    () => (localStorage.getItem("hooyootracker-theme") as Theme) || "dark",
  );

  useEffect(() => {
    if (theme === "dark") {
      document.documentElement.classList.add("dark");
      localStorage.setItem("hooyootracker-theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("hooyootracker-theme", "light");
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme(theme === "light" ? "dark" : "light");
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

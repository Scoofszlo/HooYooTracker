import { PersistQueryClientProvider } from "@tanstack/react-query-persist-client";
import { BrowserRouter, Route, Routes } from "react-router";
import "./App.css";
import { GenericLayout } from "./components/layout/GenericLayout";
import { Snackbar } from "./components/ui/snackbar/Snackbar";
import { Home } from "./features/home";
import { ROUTES } from "./route";
import { persister, queryClient } from "./state_management/react_query";

function App() {
  return (
    <PersistQueryClientProvider
      client={queryClient}
      persistOptions={{ persister, maxAge: Infinity }}
    >
      <Snackbar />
      <BrowserRouter>
        <Routes>
          <Route path={ROUTES.HOME}>
            <Route element={<GenericLayout />}>
              <Route index element={<Home />} />
            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </PersistQueryClientProvider>
  );
}

export default App;

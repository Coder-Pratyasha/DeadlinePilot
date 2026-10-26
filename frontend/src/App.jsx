import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./components/layout/Layout";

import Dashboard from "./pages/Dashboard";
import NewPlan from "./pages/NewPlan";
import Plans from "./pages/Plans";
import PlanDetails from "./pages/PlanDetails";

function App() {
  return (
    <BrowserRouter>

      <Layout>

        <Routes>

          <Route
            path="/"
            element={<Dashboard />}
          />

          <Route
            path="/new-plan"
            element={<NewPlan />}
          />

          <Route
            path="/plans"
            element={<Plans />}
          />

          <Route
            path="/plans/:id"
            element={<PlanDetails />}
          />

        </Routes>

      </Layout>

    </BrowserRouter>
  );
}

export default App;
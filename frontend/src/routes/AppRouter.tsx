import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "../pages/Login";
import JobBoard from "../pages/JobBoard";
import RequireAuth from "../auth/RequireAuth";
import Register from "../pages/Register";
import Logout from "../pages/Logout";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes> {/* Public routes */}
        <Route path="/" element={<Navigate to="/jobs" replace />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route element={<RequireAuth />}> {/* Protected routes */ }
          <Route path="/jobs" element={<JobBoard />} />
          <Route path="/logout" element={<Logout/>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
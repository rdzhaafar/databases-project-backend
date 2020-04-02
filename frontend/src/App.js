import React from "react";
import "./App.css";
import "antd/dist/antd.css";
import "./index.css";
import { Router } from "@reach/router";
import { Home, Login } from "./pages";

const App = () => (
  <Router>
    <Home path="/" />
    <Login path="account/login" type="account" />
    <Login path="employee/login" type="employee" />
  </Router>
);

export default App;

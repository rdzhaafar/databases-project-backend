import React from "react";
import "./App.css";
import "antd/dist/antd.css";
import "./index.css";
import { Router } from "@reach/router";
import { Home, Login } from "./pages";

const App = () => (
  <Router>
    <Home path="/" />
    <Login path="login" />
  </Router>
);

export default App;

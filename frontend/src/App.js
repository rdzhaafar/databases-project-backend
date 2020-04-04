import React from "react";
import "./App.css";
import "antd/dist/antd.css";
import "./index.css";
import { Router } from "@reach/router";
import { Home, Login } from "./pages";
import AccountListing from "./pages/AccountListings";
import EmployeeListing from "./pages/EmployeeListings";
import Available from "./pages/Available";

const App = () => (
  <Router>
    <Home path="/" />
    <Login path="account/login" type="account" />
    <Login path="employee/login" type="employee" />
    <Available path="account/available" />
    <AccountListing path="account/listings" />
    <EmployeeListing path="employee/listings" />
  </Router>
);

export default App;

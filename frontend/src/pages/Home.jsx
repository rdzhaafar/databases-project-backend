import React from "react";
import { Button } from "antd";
import { Link } from "@reach/router";

import resort from "../assets/resort.jpg";

const Home = () => {
  return (
    <div className="App" style={{ backgroundImage: `url(${resort})` }}>
      <Button>
        <Link to="login">Login</Link>
      </Button>
    </div>
  );
};

export default Home;

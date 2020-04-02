import React, { useEffect, useState } from "react";
import { Spin } from "antd";
import AppLayout from "../components/AppLayout";
import axios from "axios";

import config from "../config.js";
const { backendAddress } = config;

const EmployeeListing = () => {
  const [data, setData] = useState(null);
  const [load, setLoad] = useState(false);

  useEffect(() => {
    const getListings = async () => {
      const { data } = await axios.get(backendAddress + "rentalproperty/get");
      console.log(data);
      setLoad(true);
    };

    getListings();
  }, []);

  if (!load) {
    return (
      <Spin tip="Loading...">
        <AppLayout>dimme</AppLayout>
      </Spin>
    );
  }

  return <AppLayout></AppLayout>;
};

export default EmployeeListing;

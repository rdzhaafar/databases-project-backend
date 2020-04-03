import React, { useEffect, useState } from "react";
import { Spin, Table, Descriptions } from "antd";
import AppLayout from "../components/AppLayout";
import axios from "axios";

import config from "../config.js";
const { backendAddress } = config;

const EmployeeListing = () => {
  const [data, setData] = useState(null);
  const [load, setLoad] = useState(false);

  useEffect(() => {
    const getListings = async () => {
      const { data } = await axios.get(
        backendAddress + "rentalproperty/listings"
      );
      console.log(data);

      const parsedData = data.map(property => {
        let aproperty = {
          account_id: 1,
          account_password: "password",
          bathroom: 1,
          bed: { double: 0, king: 0, queen: 0, twin: 1 },
          bedroom: 1,
          city: "Milford",
          country: "Australia",
          email: "Brandon.Gomez0@uottawa.ca",
          first_name: "Brandon",
          last_name: "Gomez",
          owner_id: 1,
          phone: "555-555-5555",
          pricing_id: 1,
          property_id: 1,
          property_type: "Residential",
          room_type: "Shared Room",
          state_province: "Ontario",
          street: "Maple Lane",
          street_no: 2879,
          unit: 220,
          username: "BrandonGomez0",
          zip: "55076"
        };

        return {
          key: property.property_id,
          id: property.property_id,
          owner: property.first_name + " " + property.last_name,
          address: property.street_no + " " + property.street,
          price: property.price,
          unit: property.unit,
          city: property.city,
          province: property.state_province,
          country: property.country,
          zip: property.zip,
          bedrooms: property.bedroom,
          beds: property.bed,
          amenities: property.amenities,
          bathroom: property.bathroom,
          className: property.class_name,
          homeType: property.home_type,
          propertyType: property.property_type,
          roomType: property.room_type,
          rules: property.rules
        };
      });
      console.log(parsedData);

      setLoad(true);
      setData(parsedData);
    };

    getListings();
  }, []);

  const columns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id"
    },
    {
      title: "Owner",
      dataIndex: "owner",
      key: "owner"
    },
    {
      title: "Price",
      dataIndex: "price",
      key: "price",
      render: text => <> {"$" + text}</>
    },
    {
      title: "Address",
      dataIndex: "address",
      key: "address"
    },
    {
      title: "Unit",
      dataIndex: "unit",
      key: "unit"
    },
    {
      title: "City",
      dataIndex: "city",
      key: "city"
    },
    {
      title: "Province/State",
      dataIndex: "province",
      key: "province"
    },
    {
      title: "Country",
      dataIndex: "country",
      key: "country"
    },
    {
      title: "ZIP",
      dataIndex: "zip",
      key: "zip"
    }
  ];

  if (!load) {
    return (
      <Spin tip="Loading...">
        <AppLayout></AppLayout>
      </Spin>
    );
  }

  return (
    <AppLayout>
      <Table
        bordered
        columns={columns}
        dataSource={data}
        expandable={{
          expandedRowRender: record => {
            const beds = Object.entries(record.beds).map(bed => {
              console.log(bed);

              return (
                <>
                  {bed[0].charAt(0).toUpperCase() +
                    bed[0].slice(1) +
                    ": " +
                    bed[1]}
                  <br />
                </>
              );
            });
            return (
              <div style={{ backgroundColor: "#fff", padding: "20px 15px" }}>
                <Descriptions title="Listing Info" bordered>
                  <Descriptions.Item label="Class">
                    {record.className}
                  </Descriptions.Item>
                  <Descriptions.Item label="Home Type">
                    {record.homeType}
                  </Descriptions.Item>
                  <Descriptions.Item label="Property Type">
                    {record.propertyType}
                  </Descriptions.Item>
                  <Descriptions.Item label="Room Type">
                    {record.roomType}
                  </Descriptions.Item>
                  <Descriptions.Item label="Bedrooms">
                    {record.bedrooms}
                  </Descriptions.Item>
                  <Descriptions.Item label="Beds">{beds}</Descriptions.Item>
                  <Descriptions.Item label="Bathrooms">
                    {record.bathroom}
                  </Descriptions.Item>
                  <Descriptions.Item label="Amenities">
                    {record.amenities}
                  </Descriptions.Item>
                  <Descriptions.Item label="Rules">
                    {record.rules}
                  </Descriptions.Item>
                </Descriptions>
              </div>
            );
          }
        }}
      />
    </AppLayout>
  );
};

export default EmployeeListing;

import React, { useEffect, useState } from "react";
import {
  Spin,
  Table,
  Descriptions,
  Row,
  Col,
  Button,
  Calendar,
  Card,
} from "antd";
import AppLayout from "../components/AppLayout";
import axios from "axios";
import moment from "moment";

import config from "../config.js";
import Title from "antd/lib/typography/Title";
import { navigate } from "@reach/router";
const { backendAddress } = config;

const Available = () => {
  document.title = "Available Listings";

  const [data, setData] = useState(null);
  const [load, setLoad] = useState(false);
  const [loadCalender, setLoadCalender] = useState(false);
  const [expandedRows, setexpandedRows] = useState([]);
  const [unavailDates, setUnavailDates] = useState({});

  useEffect(() => {
    const getListings = async () => {
      const { data } = await axios.get(
        backendAddress + "rentalproperty/listings"
      );

      const parsedData = data.map((property) => {
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
          rules: property.rules,
        };
      });

      setData(parsedData);
      setLoad(true);
    };

    getListings();
  }, []);

  useEffect(() => {
    setLoadCalender(false);

    const getUnavailDates = async (property) => {
      const { data } = await axios.post(backendAddress + "rentaldate/get", {
        property_id: property,
      });

      const dates = data.map(({ rental_date }) => moment(rental_date));

      let temp = unavailDates;
      temp[property] = dates;

      setUnavailDates(temp);
    };

    expandedRows.forEach((rowId) => {
      getUnavailDates(rowId);
    });

    setTimeout(() => {
      setLoadCalender(true);
    }, 200);
  }, [expandedRows, unavailDates]);

  const columns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
    },
    {
      title: "Price",
      dataIndex: "price",
      key: "price",
      render: (text) => <> {"$" + text}</>,
    },
    {
      title: "Address",
      dataIndex: "address",
      key: "address",
    },
    {
      title: "City",
      dataIndex: "city",
      key: "city",
    },
    {
      title: "Province/State",
      dataIndex: "province",
      key: "province",
    },
    {
      title: "Country",
      dataIndex: "country",
      key: "country",
    },
    {
      title: "Owner",
      dataIndex: "owner",
      key: "owner",
    },
  ];

  const onExpand = (expandedRows) => {
    setexpandedRows(expandedRows);
  };

  if (!load) {
    return (
      <Spin tip="Loading...">
        <AppLayout></AppLayout>
      </Spin>
    );
  }

  return (
    <AppLayout>
      <Row>
        <Col span={16}>
          <Title>Available Listings</Title>
        </Col>
        <Col flex={1}>
          <Button
            style={{ float: "right" }}
            type="primary"
            onClick={() => navigate("/account/listings")}
          >
            Your Listings
          </Button>
        </Col>
      </Row>
      <Table
        bordered
        columns={columns}
        dataSource={data}
        expandable={{
          expandedRowRender: (record) => {
            const beds = Object.entries(record.beds).map((bed) => {
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
                <Row key={record.key + "r"}>
                  <Col span={18}>
                    <Descriptions
                      key={record.key + "d"}
                      title="Listing Info"
                      bordered
                      column={2}
                    >
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
                  </Col>
                  <Col span={6}>
                    <Card title="Available Dates">
                      {loadCalender ? (
                        <Calendar
                          fullscreen={false}
                          disabledDate={(date) => {
                            let unavail = false;

                            if (unavailDates[record.id]) {
                              unavailDates[record.id].forEach((unavailDate) => {
                                if (
                                  moment(date).format("YYYY MM DD") ===
                                  moment(unavailDate).format("YYYY MM DD")
                                ) {
                                  unavail = true;
                                }
                              });

                              return unavail;
                            } else return true;
                          }}
                        />
                      ) : (
                        <Spin>
                          <Calendar fullscreen={false} />
                        </Spin>
                      )}
                    </Card>
                  </Col>
                </Row>
              </div>
            );
          },
          onExpandedRowsChange: onExpand,
        }}
        pagination={{ pageSize: 12 }}
      />
    </AppLayout>
  );
};

export default Available;

import React, { useEffect, useState } from "react";
import {
  Spin,
  Row,
  Col,
  Button,
  Form,
  Input,
  Card,
  Select,
  Divider,
  Descriptions,
} from "antd";
import AppLayout from "../components/AppLayout";
import axios from "axios";

import config from "../config.js";
import { navigate } from "@reach/router";

import Title from "antd/lib/typography/Title";
import { PlusCircleTwoTone } from "@ant-design/icons";
import Paragraph from "antd/lib/typography/Paragraph";
const { Option } = Select;
const { backendAddress } = config;

const NewListings = () => {
  const [data, setData] = useState(null);
  const [load, setLoad] = useState(false);
  const [pricingSelected, setPricingSelected] = useState(null);
  const [modal, setModal] = useState(false);

  useEffect(() => {
    const getPricings = async () => {
      const { data } = await axios.post(backendAddress + "pricing/get", {
        host: localStorage.getItem("accountId"),
      });
      setData(data);
      setLoad(true);
    };

    getPricings();
  }, []);

  const generatePricingOptions = () => {
    console.log(data);

    return data.map((pricing) => {
      return (
        <Option key={pricing.pricing_id}>
          <Descriptions size="small">
            <Descriptions.Item label="Name">
              {pricing.class_name}
            </Descriptions.Item>
            <Descriptions.Item label="Home Type">
              {pricing.home_type}
            </Descriptions.Item>
            <Descriptions.Item label="Price">{pricing.price}</Descriptions.Item>
            <Descriptions.Item label="Accomodates">
              {pricing.accomodates}
            </Descriptions.Item>
            <Descriptions.Item label="Amenities">
              {pricing.amenities.split(",").map((amenity) => {
                return (
                  <>
                    {amenity}
                    <br />
                  </>
                );
              })}
            </Descriptions.Item>
            <Descriptions.Item label="Rules">
              <Paragraph ellipsis>
                {pricing.rules.split(",").map((rule) => {
                  return (
                    <>
                      {rule}
                      <br />
                    </>
                  );
                })}
              </Paragraph>
            </Descriptions.Item>
          </Descriptions>
        </Option>
      );
    });
  };

  const onFinish = (values) => {
    console.log("Success:", values);
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
          <Title>New Listing</Title>
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
      <Card title="1. Select Class">
        <Form
          name="classForm"
          initialValues={{ remember: true }}
          labelCol={{ span: 2 }}
          wrapperCol={{ span: 20 }}
        >
          <Form.Item label="Class" name="class" rules={[{ required: true }]}>
            <Select
              defaultOpen
              placeholder="Select Class to continue"
              onChange={(val) => setPricingSelected(parseInt(val))}
              dropdownRender={(menu) => (
                <>
                  {menu}
                  <Divider style={{ margin: "4px 0" }} />
                  <Button
                    type="dashed"
                    style={{ marginLeft: "5px" }}
                    onClick={() => setModal(true)}
                  >
                    <PlusCircleTwoTone />
                    Add Listing
                  </Button>
                </>
              )}
            >
              {generatePricingOptions()}
            </Select>
          </Form.Item>
        </Form>
      </Card>
      <Card
        title="2. Enter Listing Details"
        style={pricingSelected == null ? { backgroundColor: "#aaa" } : {}}
      >
        <Form
          name="listingForm"
          initialValues={{ remember: true }}
          labelCol={{ span: 2 }}
          wrapperCol={{ span: 16 }}
        >
          <Form.Item
            label="Username"
            name="username"
            rules={[{ required: true, message: "Please input your username!" }]}
          >
            <Input disabled={pricingSelected == null} />
          </Form.Item>
        </Form>
      </Card>
    </AppLayout>
  );
};

export default NewListings;

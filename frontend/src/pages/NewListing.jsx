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
  Modal,
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
  const [accom, setAccom] = useState(0);

  const [pricingForm] = Form.useForm();

  useEffect(() => {
    const getPricings = async () => {
      const { data } = await axios.post(backendAddress + "pricing/get", {
        host: localStorage.getItem("accountId"),
      });
      setData(data);
      setLoad(true);
    };

    getPricings();
  }, [modal]);

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
  const onPricingFinish = (values) => {
    console.log("Success Pricing:", values);

    const pricing = values;
    pricing.host = localStorage.getItem("accountId");

    const setPricing = async () => {
      await axios.post(backendAddress + "pricing/new", pricing);

      setModal(false);
    };
    setPricing();
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
          hideRequiredMark
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
                  <Button type="dashed" block onClick={() => setModal(true)}>
                    <PlusCircleTwoTone />
                    Add Class
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
      <Modal
        title="New Class"
        visible={modal}
        onCancel={() => setModal(false)}
        onOk={() => pricingForm.submit()}
      >
        <Form
          form={pricingForm}
          name="pricing"
          initialValues={{ remember: true }}
          labelCol={{ span: 5 }}
          wrapperCol={{ span: 16 }}
          onFinish={onPricingFinish}
          hideRequiredMark
        >
          <Form.Item
            label="Name"
            name="class_name"
            rules={[{ required: true, message: "Please enter a name" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Home Type"
            name="home_type"
            rules={[{ required: true, message: "Please enter a home type" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Price"
            name="price"
            rules={[{ required: true, message: "Please enter a price" }]}
          >
            <Input type="number" prefix="$" />
          </Form.Item>
          <Form.Item
            label="Accomodates"
            name="accomodates"
            rules={[
              { required: true, message: "Please enter number of people" },
            ]}
            shouldUpdate
          >
            <Input
              onChange={(e) => setAccom(e.target.value)}
              defaultValue={accom}
              type="number"
              suffix={accom < 2 ? "person" : "people"}
            />
          </Form.Item>
          <Form.Item
            label="Amenities"
            name="amenities"
            rules={[{ required: true, message: "Please enter amenities" }]}
          >
            <Input.TextArea />
          </Form.Item>
          <Form.Item
            label="Rules"
            name="rules"
            rules={[{ required: true, message: "Please enter rules" }]}
          >
            <Input.TextArea />
          </Form.Item>
        </Form>
      </Modal>
    </AppLayout>
  );
};

export default NewListings;

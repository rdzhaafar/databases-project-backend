import React, { useEffect, useState } from "react";
import {
  Spin,
  Row,
  Col,
  Button,
  Form,
  Input,
  Select,
  Divider,
  Descriptions,
  Modal,
  InputNumber,
  Collapse,
} from "antd";
import AppLayout from "../components/AppLayout";
import axios from "axios";

import config from "../config.js";
import { navigate } from "@reach/router";

import Title from "antd/lib/typography/Title";
import { PlusCircleTwoTone, LeftCircleTwoTone } from "@ant-design/icons";
import Paragraph from "antd/lib/typography/Paragraph";
const { Option } = Select;
const { Panel } = Collapse;
const { backendAddress } = config;

const NewListings = () => {
  document.title = "New Listing";

  const [data, setData] = useState(null);
  const [countries, setCountries] = useState([]);
  const [load, setLoad] = useState(false);
  const [sending, setSending] = useState(false);
  const [pricingSelected, setPricingSelected] = useState(null);
  const [modal, setModal] = useState(false);
  const [accom, setAccom] = useState(1);
  const [collKey, setCollKey] = useState(["class"]);

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

  useEffect(() => {
    const getBranch = async () => {
      const { data: countries } = await axios.get(
        backendAddress + "branch/get"
      );
      setCountries(countries);
    };
    getBranch();
  }, []);

  const generatePricingOptions = () => {
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

  const generateCountryOptions = () => {
    return countries.map((country) => (
      <Option key={country.country}>{country.country}</Option>
    ));
  };

  const onListingFinish = (values) => {
    const addListing = async (listing) => {
      await axios.post(backendAddress + "rentalproperty/new", listing);
      setSending(false);
      navigate("../listings");
    };
    setSending(true);

    const listing = values;
    listing.pricing_id = pricingSelected;
    listing.owner_id = parseInt(localStorage.getItem("accountId"));
    listing.bed = JSON.stringify(values.bed);
    console.log(listing);

    addListing(listing);
  };

  const onPricingFinish = (values) => {
    console.log("Success Pricing:", values);

    const pricing = values;
    pricing.host = localStorage.getItem("accountId");

    const setPricing = async () => {
      await axios.post(backendAddress + "pricing/new", pricing);

      pricingForm.resetFields();
      setModal(false);
    };
    setPricing();
  };

  const onCollChange = (e) => {
    console.log(e);

    setCollKey(e);
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
            <LeftCircleTwoTone />
            Back to Your Listings
          </Button>
        </Col>
      </Row>
      <Collapse activeKey={collKey} onChange={onCollChange}>
        <Panel key="class" header="1. Select Class">
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
                autoFocus
                placeholder="Select Class to continue"
                onChange={(val) => {
                  setPricingSelected(parseInt(val));
                  setCollKey(["class", "listing"]);
                }}
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
        </Panel>
        <Panel
          key="listing"
          header="2. Enter Listing Details"
          disabled={pricingSelected == null}
        >
          <Form
            name="listingForm"
            initialValues={{ remember: true }}
            labelCol={{ span: 3 }}
            wrapperCol={{ span: 16 }}
            onFinish={onListingFinish}
          >
            <Form.Item
              label="Street No."
              name="street_no"
              rules={[
                { required: true, message: "Please enter a street number" },
                { type: "number", min: 1, message: "Invalid street number" },
              ]}
            >
              <InputNumber disabled={pricingSelected == null} />
            </Form.Item>
            <Form.Item
              label="Street"
              name="street"
              rules={[
                { required: true, message: "Please enter a street name" },
              ]}
            >
              <Input disabled={pricingSelected == null} />
            </Form.Item>
            <Form.Item
              label="Unit"
              name="unit"
              rules={[
                { required: true, message: "Please enter a unit number" },
                { type: "number", min: 0, message: "Invalid unit number" },
              ]}
            >
              <InputNumber disabled={pricingSelected == null} />
            </Form.Item>
            <Form.Item
              label="City"
              name="city"
              rules={[{ required: true, message: "Please enter a city" }]}
            >
              <Input disabled={pricingSelected == null} />
            </Form.Item>
            <Form.Item
              label="Province/State"
              name="state_province"
              rules={[
                { required: true, message: "Please enter a Province/State" },
              ]}
            >
              <Input disabled={pricingSelected == null} />
            </Form.Item>
            <Form.Item
              label="Country"
              name="country"
              rules={[{ required: true, message: "Please select a Country" }]}
            >
              <Select
                placeholder="Select Country"
                showSearch
                filterOption={(input, option) =>
                  option.children.toLowerCase().indexOf(input.toLowerCase()) >=
                  0
                }
              >
                {generateCountryOptions()}
              </Select>
            </Form.Item>
            <Form.Item
              label="ZIP"
              name="zip"
              rules={[{ required: true, message: "Please enter a ZIP" }]}
            >
              <Input disabled={pricingSelected == null} />
            </Form.Item>
            <Form.Item
              label="Property Type"
              name="property_type"
              rules={[
                { required: true, message: "Please enter a property type" },
              ]}
            >
              <Input disabled={pricingSelected == null} />
            </Form.Item>
            <Form.Item
              label="Room Type"
              name="room_type"
              rules={[{ required: true, message: "Please enter a room type" }]}
            >
              <Input disabled={pricingSelected == null} />
            </Form.Item>
            <Form.Item
              label="Bathrooms"
              name="bathroom"
              rules={[
                {
                  required: true,
                  message: "Please enter a number of bathroom",
                },
                { type: "number", min: 1, message: "Invalid number" },
              ]}
            >
              <InputNumber disabled={pricingSelected == null} />
            </Form.Item>
            <Form.Item
              label="Bedrooms"
              name="bedroom"
              rules={[
                { required: true, message: "Please enter a number of bedroom" },
                { type: "number", min: 1, message: "Invalid number" },
              ]}
            >
              <InputNumber disabled={pricingSelected == null} />
            </Form.Item>
            <Divider orientation="left">Beds</Divider>
            <Form.Item
              label="Twin"
              name={["bed", "twin"]}
              rules={[
                {
                  required: true,
                  message: "Please enter a number of twin beds",
                },
                { type: "number", min: 0, message: "Invalid number" },
              ]}
            >
              <InputNumber disabled={pricingSelected == null} />
            </Form.Item>
            <Form.Item
              label="Double"
              name={["bed", "double"]}
              rules={[
                {
                  required: true,
                  message: "Please enter a number of double beds",
                },
                { type: "number", min: 0, message: "Invalid number" },
              ]}
            >
              <InputNumber disabled={pricingSelected == null} />
            </Form.Item>
            <Form.Item
              label="Queen"
              name={["bed", "queen"]}
              rules={[
                {
                  required: true,
                  message: "Please enter a number of queen beds",
                },
                { type: "number", min: 0, message: "Invalid number" },
              ]}
            >
              <InputNumber disabled={pricingSelected == null} />
            </Form.Item>
            <Form.Item
              label="King"
              name={["bed", "king"]}
              rules={[
                {
                  required: true,
                  message: "Please enter a number of king beds",
                },
                { type: "number", min: 0, message: "Invalid number" },
              ]}
            >
              <InputNumber disabled={pricingSelected == null} />
            </Form.Item>
            <Form.Item
              wrapperCol={{
                xs: { span: 24, offset: 0 },
                sm: { span: 16, offset: 3 },
              }}
            >
              <Button
                type="primary"
                htmlType="submit"
                block
                disabled={pricingSelected == null}
                loading={sending}
              >
                <PlusCircleTwoTone />
                Add Listing
              </Button>
            </Form.Item>
          </Form>
        </Panel>
      </Collapse>
      <Modal
        title="New Class"
        visible={modal}
        onCancel={() => setModal(false)}
        onOk={() => pricingForm.submit()}
      >
        <Form
          form={pricingForm}
          name="pricing"
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
            rules={[
              { required: true, message: "Please enter a price" },
              {
                type: "number",
                min: 0.01,
                step: 0.01,
                message: "Price is too low",
              },
            ]}
          >
            <InputNumber
              defaultValue={1}
              formatter={(value) => `$${value}`}
              min={0.01}
              step={1}
            />
          </Form.Item>
          <Form.Item
            label="Accomodates"
            name="accomodates"
            rules={[
              { required: true, message: "Please enter number of people" },
              { type: "number", min: 1, message: "Must accomodate at least 1" },
            ]}
            shouldUpdate
          >
            <InputNumber
              onChange={(value) => setAccom(value)}
              defaultValue={accom}
              min={1}
              formatter={(value) =>
                `${value} ${accom < 2 ? "person" : "people"}`
              }
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

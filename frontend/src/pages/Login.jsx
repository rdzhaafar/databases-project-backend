import React, { useState, useEffect } from "react";
import {
  Row,
  Col,
  Typography,
  Form,
  Input,
  Button,
  Checkbox,
  Card,
  Divider,
  Alert
} from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import { navigate } from "@reach/router";
import axios from "axios";

import config from "../config.js";
import resort from "../assets/resort.jpg";

const { backendAddress } = config;
const { Title } = Typography;

const Login = props => {
  const [loading, setLoading] = useState(false);
  const [badCreds, setBadCreds] = useState(false);

  const type = props.type;

  useEffect(() => localStorage.clear(), []);

  const onFinish = values => {
    setLoading(true);

    let loginCreds = {};
    if (type === "employee") {
      loginCreds.employee_username = values.username;
    } else {
      loginCreds.username = values.username;
    }
    loginCreds[type + "_password"] = values.password;

    axios
      .post(backendAddress + type + "/login", loginCreds)
      .then(({ data }) => {
        if (type === "account") {
          localStorage.setItem("accountId", data.account_id);
          localStorage.setItem("name", data.first_name + " " + data.last_name);
        } else if (type === "employee") {
          localStorage.setItem("accountId", data.employee_id);
          localStorage.setItem("name", data.employee_username);
        }
        setLoading(false);
        navigate("listings");
      })
      .catch(err => {
        if (err.response && err.response.status === 400) {
          setLoading(false);
          setBadCreds(true);
        } else {
          console.error(err);
        }
      });
  };

  return (
    <div style={{ backgroundImage: `url(${resort})` }}>
      <Row
        type="flex"
        justify="center"
        align="middle"
        style={{ minHeight: "100vh" }}
      >
        <Card>
          <Row justify="space-around" align="middle">
            <Col xs={24} lg={11}>
              <Row type="flex" justify="center" align="middle">
                {type === "account" ? (
                  <Title>Welcome to [INSERT GENERIC NAME HERE]</Title>
                ) : (
                  <Title>Employee Sign In</Title>
                )}
              </Row>
              {badCreds ? (
                <Row>
                  <Col flex={1}>
                    <Alert
                      message="Let's try that again"
                      description="Either the username or password is incorrect. Please try again."
                      type="error"
                      showIcon
                    />
                  </Col>
                </Row>
              ) : null}
            </Col>
            <Col xs={0} lg={2}>
              <Row type="flex" justify="space-around" align="middle">
                <Divider type="vertical" style={{ height: "140px" }} />
              </Row>
            </Col>
            <Col xs={24} lg={11}>
              <Row type="flex" justify="space-around" align="middle">
                <Form
                  initialValues={{ remember: true }}
                  onFinish={onFinish}
                  style={{ width: "400px" }}
                >
                  <Form.Item
                    name="username"
                    rules={[
                      { required: true, message: "Please input your Username!" }
                    ]}
                  >
                    <Input
                      prefix={<UserOutlined className="site-form-item-icon" />}
                      placeholder="Username"
                    />
                  </Form.Item>
                  <Form.Item
                    name="password"
                    rules={[
                      { required: true, message: "Please input your Password!" }
                    ]}
                  >
                    <Input
                      prefix={<LockOutlined className="site-form-item-icon" />}
                      type="password"
                      placeholder="Password"
                    />
                  </Form.Item>
                  <Form.Item name="remember" valuePropName="checked" noStyle>
                    <Checkbox style={{ marginBottom: "18px" }}>
                      Remember me
                    </Checkbox>
                  </Form.Item>

                  <Form.Item style={{ margin: 0 }}>
                    <Button
                      type="primary"
                      htmlType="submit"
                      block
                      loading={loading}
                    >
                      Log in
                    </Button>
                    {/* Or <a href="">register now!</a> */}
                  </Form.Item>
                </Form>
              </Row>
            </Col>
          </Row>
        </Card>
      </Row>
    </div>
  );
};

export default Login;

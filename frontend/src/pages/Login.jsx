import React from "react";
import {
  Row,
  Col,
  Typography,
  Form,
  Input,
  Button,
  Checkbox,
  Card,
  Divider
} from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";

import resort from "../assets/resort.jpg";

const { Title } = Typography;

const Login = () => {
  const onFinish = values => {
    console.log("Received values of form: ", values);
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
          <Row type="flex" justify="center" align="middle">
            <Col xs={24} lg={11}>
              <Row type="flex" justify="center" align="middle">
                <Title>Welcome to [INSERT GENERIC NAME HERE]</Title>
              </Row>
            </Col>
            <Col xs={0} lg={2}>
              <Divider type="vertical" style={{ height: "140px" }} />
            </Col>
            <Col xs={24} lg={11}>
              <Form
                initialValues={{ remember: true }}
                onFinish={onFinish}
                style={{ width: "500px" }}
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
                <Form.Item>
                  <Form.Item name="remember" valuePropName="checked" noStyle>
                    <Checkbox>Remember me</Checkbox>
                  </Form.Item>

                  <a style={{ float: "right" }}>Forgot password</a>
                </Form.Item>

                <Form.Item>
                  <Button type="primary" htmlType="submit" block>
                    Log in
                  </Button>
                  {/* Or <a href="">register now!</a> */}
                </Form.Item>
              </Form>
            </Col>
          </Row>
        </Card>
      </Row>{" "}
    </div>
  );
};

export default Login;

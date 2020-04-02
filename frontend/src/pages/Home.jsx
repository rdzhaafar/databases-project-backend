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
  Divider,
  Alert
} from "antd";
import { Link } from "@reach/router";

import resort from "../assets/resort.jpg";

const { Title } = Typography;

const Home = () => {
  return (
    <div style={{ backgroundImage: `url(${resort})` }}>
      <Row
        type="flex"
        justify="center"
        align="middle"
        style={{ minHeight: "100vh" }}
      >
        <Card style={{ minWidth: "80%" }}>
          <Row justify="space-around" align="middle">
            <Col xs={24} lg={11}>
              <Row type="flex" justify="center" align="middle">
                <Title>Guest and Host</Title>
              </Row>
              <Row>
                <Col flex={1}>
                  <Button type="primary" block>
                    <Link to="account/login">Guest and Host Login</Link>
                  </Button>
                </Col>
              </Row>
            </Col>
            <Col xs={0} lg={2}>
              <Row type="flex" justify="space-around" align="middle">
                <Divider type="vertical" style={{ height: "140px" }} />
              </Row>
            </Col>
            <Col xs={24} lg={11}>
              <Row type="flex" justify="center" align="middle">
                <Title>Employee</Title>
              </Row>
              <Row>
                <Col flex={1}>
                  <Button type="primary" block>
                    <Link to="employee/login">Employee Login</Link>
                  </Button>
                </Col>
              </Row>
            </Col>
          </Row>
        </Card>
      </Row>
    </div>
  );
};

export default Home;

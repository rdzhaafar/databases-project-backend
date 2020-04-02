import React from "react";
import { Layout, Button } from "antd";
import {
  UserOutlined,
  LogoutOutlined,
  CompassTwoTone
} from "@ant-design/icons";
import { navigate } from "@reach/router";

const { Header, Content } = Layout;

const AppLayout = props => {
  const handleLogout = () => {
    navigate("/");
  };

  const name = localStorage.getItem("name");
  if (name == null) navigate("/");

  return (
    <Layout>
      <Header style={{ paddingLeft: "12px" }}>
        <CompassTwoTone
          spin
          style={{ fontSize: "40px", marginTop: "12px" }}
          onClick={() => navigate("/")}
        />
        <div className="logo" style={{ float: "right" }}>
          <Button>
            <UserOutlined /> {name}
          </Button>
          <Button onClick={handleLogout}>
            <LogoutOutlined /> Logout
          </Button>
        </div>
      </Header>
      <Layout>
        <Content
          style={{
            padding: "20px 15px",
            margin: 0,
            minHeight: 280
          }}
        >
          {props.children}
        </Content>
      </Layout>
    </Layout>
  );
};
export default AppLayout;

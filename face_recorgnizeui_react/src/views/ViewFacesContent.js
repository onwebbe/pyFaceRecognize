import React from 'react';
import { Layout, Menu, Button } from 'antd';
import { UploadOutlined, UserOutlined, VideoCameraOutlined } from '@ant-design/icons';
import FaceTable from '../component/FaceTable'
const { Header, Content, Footer, Sider } = Layout;
function ViewFacesContent() {
    return (
        <Layout>
            <div style={{textAlign: 'left'}}>
                <span className="">一共 312 张脸</span>
                <span className="" style={{display:'inline-block',float:'right'}}>
                    <Button style={{marginRight: '15px'}}>取消</Button>
                    <Button type="primary">保存</Button>
                </span>
            </div>
            <div>
                <FaceTable></FaceTable>
            </div>
        </Layout>
    );
}
export default ViewFacesContent;
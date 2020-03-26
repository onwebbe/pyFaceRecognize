import React from 'react';
import { RetweetOutlined, RollbackOutlined } from '@ant-design/icons';
import { Layout, Select, Button } from 'antd';
import { UploadOutlined, UserOutlined, VideoCameraOutlined } from '@ant-design/icons';
import PersonCard from '../component/PersonCard'
import axios from 'axios';
const { Header, Content, Footer, Sider } = Layout;
class ViewPersonCardList extends React.Component {
    constructor(props) {
        super(props);
        this.props = props;
        this.state = {
            personDetailList: []
        }
        this.refreshPersonList = this.refreshPersonList.bind(this);
    }
    componentDidMount() {
        this.refreshPersonList();
    }
    refreshPersonList() {
        return new Promise(resolve => {
            axios.get('/api/v1/facerecorgnize/getPersonDetailList')
            .then((response) => {
              var responseData = response.data;
              this.setState({
                personDetailList: responseData.data
              });
            })
            .catch((error) => {
              console.log(error);
            })
        });
    }
    render() {
        var personCardList = []
        for (var i = 0; i < this.state.personDetailList.length; i++) {
            var personData = this.state.personDetailList[i];
            console.log(personData)
            personCardList.push(<PersonCard key={personData.personId}  personDetails={personData}></PersonCard>)
        }
        var name = 'test'
        return (
            <Layout>
                <div style={{textAlign: 'center'}}>
                    <span>
                        人物列表
                    </span>
                </div>
                <div style={{textAlign: 'left'}}>
                    {personCardList}
                </div>
            </Layout>
        );
    }
}
export default ViewPersonCardList;
import React from 'react';
import { RetweetOutlined, RollbackOutlined } from '@ant-design/icons';
import { Layout, Select, Button } from 'antd';
import { UploadOutlined, UserOutlined, VideoCameraOutlined } from '@ant-design/icons';
import FaceTable from '../component/FaceTable'
const { Header, Content, Footer, Sider } = Layout;
class ViewFacesContent extends React.Component {
    constructor(props) {
        super(props);
        this.props = props;
        this.refreshTable = this.refreshTable.bind(this);
        this.refreshSelector = this.refreshSelector.bind(this);
        this.populateFacdeTable = this.populateFacdeTable.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleBlur = this.handleBlur.bind(this);
        this.peopleDataReady = this.peopleDataReady.bind(this);

        var initialSesrchCritera = null;

        // var urlSearchParams = this.props.history.location;
        // if (urlSearchParams && urlSearchParams.state) {
        //     initialPersonList = [{
        //         key: 'personId',
        //         value: urlSearchParams.state
        //     }]
        // }

        var matches = this.props.match;
        if (matches && matches.params && matches.params.personId) {
            initialSesrchCritera = [{
                key: 'personId',
                value: [matches.params.personId]
            }]
        }

        this.state = {
            personFilterChildrenOption: [],
            personFilterSelectedValue: [],
            initialSesrchCritera: initialSesrchCritera
        }
    }
    populateFacdeTable (ref) {
        this.faceTableComponent = ref;
    }
    refreshTable() {
        this.faceTableComponent._getFaces()
    }
    refreshSelector() {
        this.faceTableComponent._getAllPerson();
        this.faceTableComponent.setSearchCriteria(null);
        this.faceTableComponent._getFaces()
    }
    handleChange(value) {
        this.setState({
            personFilterSelectedValue: value
        });
    }
    handleBlur() {
        var value = this.state.personFilterSelectedValue;
        this.faceTableComponent.setSearchCriteria([{
            key: 'personId',
            value: value
        }]);
        this.faceTableComponent._getFaces();
    }
    peopleDataReady(data) {
        var personOptionList = [];
        var personOptionValue = [];
        for(var i = 0; i < data.length; i++) {
            var person = data[i];
            var personOption = (
                <Select.Option key={person.personId} value={person.personId}>{person.personName}</Select.Option>
            );
            personOptionList.push(personOption);
            if (!this.state.initialSesrchCritera) {
                personOptionValue.push(person.personId);
            }
        }
        if (this.state.initialSesrchCritera) {
            this.state.initialSesrchCritera.forEach((item, key) => {
                item.value.forEach((personId, key) => {
                    personOptionValue.push(parseInt(personId));
                });
            });
        }
        this.setState({
            personFilterChildrenOption: personOptionList,
            personFilterSelectedValue: personOptionValue
        })
    }
    render() {
        return (
            <Layout>
                <div style={{textAlign: 'left'}}>
                    <span className="">
                        <Select
                            mode="multiple"
                            placeholder="选择"
                            style={{ width: 'calc(100% - 250px)' }}
                            removeIcon={false}
                            onChange={this.handleChange}
                            onBlur={this.handleBlur}
                            value={this.state.personFilterSelectedValue}
                        >
                            {this.state.personFilterChildrenOption}
                        </Select>
                    </span>
                    <span className="" style={{display:'inline-block',float:'right'}}>
                        <Button type="" style={{marginRight: '15px'}} icon={<RollbackOutlined />}  onClick={this.refreshSelector}>重置过滤</Button>
                        <Button type="" style={{marginRight: '15px'}} icon={<RetweetOutlined />}  onClick={this.refreshTable}>刷新</Button>
                    </span>
                </div>
                <div>
                    <FaceTable searchCriteria={this.state.initialSesrchCritera} populateFacdeTable={this.populateFacdeTable} informFaceContentPeopleDataReady={this.peopleDataReady}></FaceTable>
                </div>
            </Layout>
        );
    }
}
export default ViewFacesContent;
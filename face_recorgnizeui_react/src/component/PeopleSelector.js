
import React from 'react';
import { Select, Divider, Input } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import axios from 'axios';
import { OmitProps } from 'antd/lib/transfer/renderListBody';
const { Option } = Select;


function onChange() {}
function onBlur() {}
function onSearch() {}
class PeopleSelector extends React.Component {
  constructor(props) {
    super(props);
    this.props = props;
    this.state = {
      newPersonName: '',
      personId: this.props.personId
    }
    this.onNameChange = this.onNameChange.bind(this);
    this.addFace = this.addFace.bind(this);
    this.onChange = this.onChange.bind(this);
  }
  async componentDidMount() {
    // await this._getAllPerson();
    // await this._getPersonById(this.props.personId);
  }
  addFace() {
    var self = this;
    axios.get('/api/v1/facerecorgnize/addNewPersonFace?faceId=' + this.props.faceId + '&personName=' + this.state.newPersonName)
    .then((response) => {
      var responseData = response.data;
      var personId = responseData.data.personId;
      self.setState({
        personId: personId
      })
      self.props.getAllPersonMethod();
    })
    .catch((error) => {
      console.log(error);
    })
  }
  onBlue() {
    // alert('blue')
  }
  onSearch() {
    // alert('search')
  }
  onChange(value) {
    var self = this;
    axios.get('/api/v1/facerecorgnize/changeFacePerson?faceId=' + this.props.faceId + '&personId=' + value)
    .then((response) => {
      // self.props.getAllPersonMethod();
      this.setState({
        personId: value 
      })
    })
    .catch((error) => {
      console.log(error);
    })
  }
  onNameChange(evt) {
    var self = this;
    var personName = evt.target.value;
    this.setState({
      newPersonName: personName
    })
  }
  _getAllPerson() {
    return new Promise(resolve => {
      axios.get('/api/v1/facerecorgnize/getPersons')
      .then((response) => {
        var personMap = response.data;
        var personList = [];
        for (var key in personMap) {
          personList.push(personMap[key]);
        }
        this.setState({
          personList: personList
        });
        resolve();
      })
      .catch((error) => {
        console.log(error);
        resolve();
      })
    });
  }
  _getPersonById(personId) {
    return new Promise(resolve => {
      axios.get('/api/v1/facerecorgnize/getPersonById?personId=' + personId)
      .then((response) => {
        var personData = response.data;
        if (personData.personId) {
          this.setState({
            personObj: personData
          });
        }
        resolve();
      })
      .catch((error) => {
        console.log(error);
        resolve();
      })
    });
  }
  render() {
    var options = [];
    for (var i = 0; i < this.props.allPersonList.length; i++) {
      var personData = this.props.allPersonList[i];
      options.push(<Option key={personData.personId} value={personData.personId}>{personData.personName}</Option>)
    }
    var name = 'test'
    return (
      <div>
      <Select
        showSearch
        value={this.state.personId}
        style={{ width: 240 }}
        placeholder="--清选择--"
        optionFilterProp="children"
        onChange={this.onChange}
        onBlur={this.onBlur}
        onSearch={this.onSearch}
        filterOption={(input, option) =>
            option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
        }
        dropdownRender={menu => (
          <div>
            {menu}
            <Divider style={{ margin: '4px 0' }} />
            <div style={{ display: 'flex', flexWrap: 'nowrap', padding: 8 }}>
              <Input style={{ flex: 'auto' }} value={this.state.newPersonName} onChange={this.onNameChange} />
              <a
                style={{ flex: 'none', padding: '8px', display: 'block', cursor: 'pointer' }}
                onClick={this.addFace}
              >
                <PlusOutlined /> 添加新的脸
              </a>
            </div>
          </div>
        )}
      >
        {options}
      </Select>
      </div>
    )
  }
}

export default PeopleSelector;

import React from 'react';
import { Select } from 'antd';
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
      personList: []
    }
  }
  async componentDidMount() {
    await this._getAllPerson();
    // await this._getPersonById(this.props.personId);
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
    for (var i = 0; i < this.state.personList.length; i++) {
      var personData = this.state.personList[i];
      options.push(<Option value={personData.personId}>{personData.personName}</Option>)
    }
    return (
      <div> {this.state.personList.forEach((personData) => (
        <span>1</span>
      ))}
      <Select defaultValue={this.props.personId} showSearch style={{ width: 200 }}
        placeholder="--清选择--"
        optionFilterProp="children"
        onChange={onChange}
        onBlur={onBlur}
        onSearch={onSearch}
        filterOption={(input, option) =>
            option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
        }
      >
        {options}
      </Select>
      </div>
    )
  }
}

export default PeopleSelector;
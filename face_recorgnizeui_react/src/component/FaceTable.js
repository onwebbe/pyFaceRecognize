import React from 'react';
import { Table, Pagination } from 'antd';
import PeopleSelector from './PeopleSelector';
import axios from 'axios';


class FaceTable extends React.Component {
    constructor(props) {
      super(props);
      var self = this;
      this.refreshPerson = this.refreshPerson.bind(this);
      this._filterData = this._filterData.bind(this);
      this.setSearchCriteria = this.setSearchCriteria.bind(this);
      this.state={
        columns: [{
          title: '标号',
          dataIndex: 'id',
          key: 'id',
          render: text => <a>{text}</a>,
        }, {
            title: '脸部图片',
            dataIndex: 'faceImage',
            key: 'faceImage',
            render: facePath => {
              if (facePath && facePath != ''){
                return (
                  <img style={{height: '50px'}} src={'/api/v1/facerecorgnize/getImage?path=' + facePath}></img>
                )
              } else {
                return (
                  <img style={{height: '50px'}}></img>
                )
              }
            }
        }, {
            title: '姓名',
            dataIndex: 'person',
            key: 'person',
            render: person => (
              <PeopleSelector key={person.faceId + person.personId} getAllPersonMethod={this.refreshPerson.bind(this)} faceId={person.faceId} personId={person.personId} allPersonList={self.state.allPeopleList}></PeopleSelector>
            )
        }],
        data: [],
        allPeopleList: [],
        currentSearchOptions: null,
        search: props.searchCriteria
      }
      
    }
    async componentDidMount() {
      this.refreshPerson();
      this.props.populateFacdeTable(this);
    }
    setSearchCriteria(search) {
      this.setState({
        search: search
      })
    }
    _filterData(data) {
      var searchCriteriaList = this.state.search;
      var searchResult = [];
      if (searchCriteriaList && searchCriteriaList.length > 0) {
        for (var i = 0; i < searchCriteriaList.length; i++) {
          var searchCriteria = searchCriteriaList[i];
          var searchKey = searchCriteria.key;
          var searchValue = searchCriteria.value;
          var isFound = false;
          var searchData = data[searchKey];
          if (searchValue instanceof Array) {
            for (var j = 0; j < searchValue.length; j++) {
              if (searchValue[j] == searchData) {
                isFound = true;
                break;
              }
            }
          } else if (searchData instanceof String) {
            if (data[searchKey] == searchValue) {
              isFound = true;
            }
          }
          searchResult[i] = isFound;
        }
        var finalResult = false;
        for (var i = 0; i < searchResult.length; i ++) {
          finalResult = finalResult || searchResult[i]
        }
        return finalResult;
      } else {
        return true;
      }
      
      
    }
    _getFaces() {
      var self = this;
      return new Promise(resolve => {
        axios.get('/api/v1/facerecorgnize/getFaces?' + new Date().getTime())
        .then((response) => {
          var faceMap = response.data;
          var faceDataList = [];
          for (var faceId in faceMap) {
            var faceItem = faceMap[faceId];
            if (self._filterData(faceItem)) {
              var faceImage = faceItem.imagePath;
              var personId = faceItem.personId;
              var faceDataObj = {
                id: faceId,
                faceImage: faceImage,
                person: {
                  personId: personId,
                  faceId: faceId
                }
              };
              faceDataList.push(faceDataObj);
            }
          }
          faceDataList = faceDataList.sort(function(a, b) {
            return b.person.personId - a.person.personId;
          });
          self.setState({
            data: faceDataList
          });

        })
        .catch((error) => {
          console.log(error);
        })
      });
    }
    async refreshPerson() {
      await this._getAllPerson();
      await this._getFaces();
    }
    _getAllPerson() {
      var self = this;
      return new Promise(resolve => {
        axios.get('/api/v1/facerecorgnize/getPersons')
        .then((response) => {
          var personMap = response.data;
          var personList = [];
          for (var key in personMap) {
            personList.push(personMap[key]);
          }
          this.setState({
            allPeopleList: personList
          });
          self.props.informFaceContentPeopleDataReady(personList);
          resolve();
        })
        .catch((error) => {
          console.log(error);
          resolve();
        })
      });
    }
    render() {
      // This syntax ensures `this` is bound within handleClick
      return (
        <div style={{marginTop: '15px'}}>
            <Table columns={this.state.columns} dataSource={this.state.data} pagination={false} rowKey={(record, index) => index}/>

            <div style={{paddingTop: '15px', textAlign: 'right'}}>
                <Pagination
                    total={85}
                    pageSize={20}
                    defaultCurrent={1}
                    />
            </div>
        </div>
      );
    }
  }

export default FaceTable;
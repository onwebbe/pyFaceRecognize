import React from 'react';
import { Table, Pagination } from 'antd';
import PeopleSelector from './PeopleSelector';
import axios from 'axios';


class FaceTable extends React.Component {
    constructor(props) {
      super(props);
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
            dataIndex: 'name',
            key: 'name',
            render: personId => (
              <PeopleSelector personId={personId}></PeopleSelector>
            )
        }],
        data: [{
          id: '1',
          faceImage: '',
          name: 'Tai'
        }, {
          id: '2',
          faceImage: '',
          name: 'Kimi'
        }]
      }
    }
    componentDidMount() {
      axios.get('/api/v1/facerecorgnize/getFacesWithName')
      .then((response) => {
        var faceMap = response.data;
        var faceDataList = [];
        for (var faceId in faceMap) {
          var faceItem = faceMap[faceId];
          var faceImage = faceItem.imagePath;
          var personId = faceItem.person ? faceItem.person.personId : '';
          var faceDataObj = {
            id: faceId,
            faceImage: faceImage,
            name: personId
          };
          faceDataList.push(faceDataObj);
        }
        this.setState({
          data: faceDataList
        });
      })
      .catch((error) => {
        console.log(error);
      })
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
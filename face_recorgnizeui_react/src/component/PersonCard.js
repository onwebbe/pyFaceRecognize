import React from 'react';
import { Card } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

class PeopleCard extends React.Component {
  constructor(props) {
    super(props);
    this.props = props;
    this.state = {
      personId: this.props.personDetails.personId,
      personName: this.props.personDetails.personName,
      imagePath: this.props.personDetails.imagePath,
      faceCount: this.props.personDetails.faceCount
    }
  }
  componentDidMount() {
    // await this._getAllPerson();
    // await this._getPersonById(this.props.personId);
  }
  render() {
    return (
      <div style={{display: 'inline-block', padding: 20 }}>
        <Card title={this.state.personName} extra={<a href={"#/faceList/" + this.state.personId}>所有脸图</a>} style={{ width: 200}}>
          <p>
          <img style={{height: '50px'}} src={'/api/v1/facerecorgnize/getImage?path=' + this.state.imagePath}></img>
          </p>
        </Card>
      </div>
    )
  }
}

export default PeopleCard;
import React from 'react';
import {HashRouter, Route, Switch, useHistory} from 'react-router-dom';
import ViewPersonCardList from '../views/ViewPersonCardList';
import ViewFacesContent from '../views/ViewFacesContent';


const BasicRoute = () => (
    <HashRouter history={useHistory}>
        <Switch>
            <Route exact path="/" component={ViewPersonCardList}/>
            <Route exact path="/personCardList" component={ViewPersonCardList}/>
            <Route exact path="/faceList/:personId" component={ViewFacesContent}/>
        </Switch>
    </HashRouter>
);


export default BasicRoute;
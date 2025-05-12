import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './components/common/Header';
import Footer from './components/common/Footer';
import Map from './components/Map/Map';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import Profile from './components/Auth/Profile';
import Checkout from './components/Payment/Checkout';
import PricingInfo from './components/Payment/PricingInfo';
import './styles.css';

const App = () => {
    return (
        <Router>
            <Header />
            <Switch>
                <Route path="/" exact component={Map} />
                <Route path="/login" component={Login} />
                <Route path="/register" component={Register} />
                <Route path="/profile" component={Profile} />
                <Route path="/checkout" component={Checkout} />
                <Route path="/pricing" component={PricingInfo} />
            </Switch>
            <Footer />
        </Router>
    );
};

export default App;
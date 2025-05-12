import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './components/common/Header';
import Footer from './components/common/Footer';
import MapContainer from './components/Map/MapContainer';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import Profile from './components/Auth/Profile';
import Checkout from './components/Payment/Checkout';
import PricingCalculator from './components/Payment/PricingCalculator';
import './styles/main.css';

const App = () => {
    return (
        <Router>
            <Header />
            <Switch>
                <Route path="/" exact component={MapContainer} />
                <Route path="/login" component={Login} />
                <Route path="/register" component={Register} />
                <Route path="/profile" component={Profile} />
                <Route path="/checkout" component={Checkout} />
                <Route path="/pricing" component={PricingCalculator} />
            </Switch>
            <Footer />
        </Router>
    );
};

export default App;
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './components/common/Header';
import Footer from './components/common/Footer';
import Map from './components/Map';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import UserProfile from './components/Auth/UserProfile';
import OrderHistory from './components/Orders/OrderHistory';
import Checkout from './components/Orders/Checkout';
import PricingCalculator from './components/Orders/PricingCalculator';

const App = () => {
  return (
    <Router>
      <Header />
      <Switch>
        <Route path="/" exact component={Map} />
        <Route path="/login" component={Login} />
        <Route path="/register" component={Register} />
        <Route path="/profile" component={UserProfile} />
        <Route path="/orders" component={OrderHistory} />
        <Route path="/checkout" component={Checkout} />
        <Route path="/pricing" component={PricingCalculator} />
      </Switch>
      <Footer />
    </Router>
  );
};

export default App;
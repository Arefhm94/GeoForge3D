import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import MapView from './pages/MapView';
import Profile from './pages/Profile';
import Orders from './pages/Orders';
import AuthForm from './components/AuthForm';
import PaymentForm from './components/PaymentForm';

function App() {
  return (
    <Router>
      <div>
        <Switch>
          <Route path="/" exact component={Dashboard} />
          <Route path="/map" component={MapView} />
          <Route path="/profile" component={Profile} />
          <Route path="/orders" component={Orders} />
          <Route path="/auth" component={AuthForm} />
          <Route path="/payment" component={PaymentForm} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
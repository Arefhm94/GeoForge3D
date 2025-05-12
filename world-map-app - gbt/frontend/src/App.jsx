import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './pages/Home';
import Signup from './pages/Signup';
import Pricing from './pages/Pricing';
import Map from './components/Map';
import SearchBar from './components/SearchBar';
import LayerSelector from './components/LayerSelector';

function App() {
    return (
        <Router>
            <div>
                <SearchBar />
                <LayerSelector />
                <Switch>
                    <Route path="/" exact component={Home} />
                    <Route path="/signup" component={Signup} />
                    <Route path="/pricing" component={Pricing} />
                    <Route path="/map" component={Map} />
                </Switch>
            </div>
        </Router>
    );
}

export default App;
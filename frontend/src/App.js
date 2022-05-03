import React, { Component } from 'react';
import { Routes, Route } from "react-router-dom";
import { ThemeProvider } from '@material-ui/core/styles';
import PodcastList from './components/podcast-list';
import PodcastPage from './components/podast-page.js';
import MyTheme from './MyTheme';
import './App.css';

class App extends Component{

  render() {
    return (
      <ThemeProvider theme={MyTheme}>
        <main>
          <Routes>
            <Route path='/' element={<PodcastList />} />
            <Route exact path='/podcasts/:id' element={<PodcastPage />} />
          </Routes>
        </main>
      </ThemeProvider>
    )
  }
}

export default App;

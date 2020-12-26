import React from "react";
//import logo from "./logo.svg";
import "./App.css";

import Content from "./content";

function App() {
    return (
        <div className="app">
            <header className="app__header">
                <h1 className="app__header__title">
                
                    Covid-19 Symptoms Tracking App on Tezos
                </h1>
            </header>
            <Content />
            <footer className="app__footer">
                <p className="app__footer__title">
                    Created for Tribe Tezos developer bootcamp
                </p>
            </footer>
        </div>
    );
}

export default App;

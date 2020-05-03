import React from "react";
import logo from "./logo.svg";
import "./App.css";
import HorseIcon from "./images/horse.svg";

import Content from "./content";

function App() {
    return (
        <div className="app">
            <header className="app__header">
                <h1 className="app__header__title">
                    <img
                        className="app__header__img"
                        alt=""
                        src={HorseIcon}
                    ></img>{" "}
                    A Betting App on Tezos
                </h1>
            </header>
            <Content />
            <footer className="app__footer">
                <p className="app__footer__title">
                    Created with ❤ for Tezos developer bootcamp
                </p>
            </footer>
        </div>
    );
}

export default App;

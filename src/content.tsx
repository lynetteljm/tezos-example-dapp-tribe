import React from "react";

import "./content.css";

const Content: React.FC = () => {
    return (
        <div className="content">
            <div className="content__column">
                <div className="content__item">
                    <div className="content__item__title">Track</div>
                    <div className="content__item__content">fast</div>
                </div>
            </div>
        </div>
    );
};

export default Content;

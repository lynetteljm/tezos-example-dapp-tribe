import React, { useState, useEffect } from "react";
import { Tezos } from "@taquito/taquito";
import { InMemorySigner } from "@taquito/signer";

import cogoToast from "cogo-toast";

import "./content.css";

type BackgroundType = {
    BackgroundId: String;
    BackgroundName: String;
};

type RecordType = {
    RecordId: String;
    RecordName: String;
};

const Content: React.FC = () => {
    const [currentTime, setCurrentTime] = useState(new Date());
    const [totalBalance, setTotalBalance] = useState<undefined | number>(
        undefined
    );
    const [CovidStatus, setCovidStatus] = useState<undefined | string>(undefined);
    const [Background, setBackground] = useState<undefined | BackgroundType[]>(undefined);
    const [Records, setRecords] = useState<undefined | RecordType[]>(undefined);

    const [changeStatusLoading, setChangeStatusLoading] = useState(false);
    const [addBackgroundLoading, setAddBackgroundLoading] = useState(false);
    const [addSympTestLoading, setAddSympTestLoading] = useState(false);

    const contractId = "KT1Jt43289yMZdSoNumf7rhoziLPKSo9GxhZ";
    Tezos.setProvider({
        rpc: "https://api.tez.ie/rpc/carthagenet",
        signer: new InMemorySigner(
            "edskS6rCh5wPWUd2D2vPRDmxnQppAr1V1e4MksLjQh1YgecFv4eYUaEYkWKFP6nYQJtopN9JT8Ms2vjoCRA4J2cUfRSe84HwZv"
        ),
    });
    const getTotalBalance = () => {
        Tezos.tz
            .getBalance(contractId)
            .then((balance) => setTotalBalance(balance.toNumber() / 1000000))
            .catch((error) => console.log(JSON.stringify(error)));
    };
    const getContractDetails = async () => {
        const contract = await Tezos.contract.at(contractId);
        const storage: any = await contract.storage();
        setCovidStatus(storage?.covidStatus);

        const Background: BackgroundType[] = [];
        const BackgroundInStorage: any = storage?.Background?.valueMap.entries();
        for (let BackgroundDetail of BackgroundInStorage) {
            for (let BackgroundInfo of BackgroundDetail){
            const id = BackgroundDetail[0];
            const BackgroundNameDetails = BackgroundInfo[1].valueMap.entries();
            let bName = "";
            for (let backgroundName of BackgroundNameDetails) {
                bName = backgroundName[1];
            }
            
            Background.push({
                BackgroundId: id,
                BackgroundName: bName,
            });
        }
        }
        setBackground(Background);
    };
    const addBackground = async () => {
        Tezos.contract
            .at(contractId)
            .then((contract) => {
                cogoToast.info("Adding background");
                setAddBackgroundLoading(true);
                return contract.methods
                    .addBackground("16", "No","510122", "Yes", "426c616168")
                    .send();
            })
            .then((op) => {
                cogoToast.info("Waiting to be confirmed");
                return op.confirmation(3).then(() => op.hash);
            })
            .then((hash) => {
                setAddBackgroundLoading(false);
                cogoToast.success("Successfully added Background");
            })
            .catch((error) => {
                setAddBackgroundLoading(false);
                console.log(JSON.stringify(error));
                cogoToast.error(
                    `Could not add background. Error:${JSON.stringify(error)}`
                );
            });
    };
    useEffect(() => {
         Tezos.setProvider({
             rpc: "https://api.tez.ie/rpc/carthagenet",
              signer: new InMemorySigner(
              "edskS6rCh5wPWUd2D2vPRDmxnQppAr1V1e4MksLjQh1YgecFv4eYUaEYkWKFP6nYQJtopN9JT8Ms2vjoCRA4J2cUfRSe84HwZv"
              ),
         });
         const interval = setInterval(() => {
             setCurrentTime(new Date());
         }, 1000);
        getTotalBalance();
        getContractDetails();
         console.log(Background);
         return () => clearInterval(interval);
    }, []);
    return (
        <div className="content">
            <div className="content__column">
                <div className="content__item">
                    <div className="content__item__title">Covid-19 Status</div>
                    <div className="content__item__content">
                        {CovidStatus !== undefined ? `${CovidStatus}` : ""}
                    </div>
                </div>
                
                <div className="content__item">
                    <div className="content__item__title">Date</div>
                    <div className="content__item__content">
                        {currentTime.getDate()}/
                        {currentTime.getMonth()}/
                        {currentTime.getFullYear()}
                    </div>
                </div>    

                <div className="content__item">
                    <div className="content__item__title">Time</div>
                    <div className="content__item__content">
                        {currentTime.getHours()}:
                        {currentTime.getMinutes() < 10 ? "0" : ""}
                        {currentTime.getMinutes()}:
                        {currentTime.getSeconds() < 10 ? "0" : ""}
                        {currentTime.getSeconds()}
                    </div>
                </div>
            </div>
            <div className="content__column">
                <div className="content__item">
                    <div className="content__item__title-wrapper">
                        <div className="content__item__title content__item__title--horses">
                            Background
                        </div>
                        <div className="content__item__title content__item__title--bets">
                            Records
                        </div>
                    </div>
                    {Background?.map((Background) => {
                        return (
                            <div className="content__item__content-wrapper">
                                <div className="content__item__content content__item__content--horses">
                                    {Background?.BackgroundName}
                                </div>
                                <div className="content__item__content content__item__content--bets">
                                    {"1"}
                                </div>
                                <div className="content__item__content content__item__content--bets">
                                    {"4"}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
            <div className="content__column content__column--action">
                <div className="content__item">
                    <button
                        className="btn btn--admin"
                        onClick={() => addBackground()}
                    >
                        {addBackgroundLoading ? (
                            <span className="loadingSpinner"></span>
                        ) : (
                            "Add Background"
                        )}
                    </button>
                </div>
                <div className="content__item">
                    <button className="btn btn--admin">
                        {addSympTestLoading ? (
                            <span className="loadingSpinner"></span>
                        ) : (
                            "Take Symptom Test"
                        )}
                    </button>
                </div>
                <div className="content__item">
                    <button className="btn btn">
                        {changeStatusLoading ? (
                            <span className="loadingSpinner"></span>
                        ) : (
                            "Change Status"
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Content;

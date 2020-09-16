import React, { useState, useEffect } from "react";
import { Tezos } from "@taquito/taquito";
import { InMemorySigner } from "@taquito/signer";

import cogoToast from "cogo-toast";

import "./content.css";

type HorseType = {
    horseId: String;
    horseName: String;
};

type BetType = {
    [sender: string]: { [horseId: string]: number };
};

const Content: React.FC = () => {
    const [currentTime, setCurrentTime] = useState(new Date());
    const [totalBalance, setTotalBalance] = useState<undefined | number>(
        undefined
    );
    const [track, setTrack] = useState<undefined | string>(undefined);
    const [horses, setHorses] = useState<undefined | HorseType[]>(undefined);
    const [bets, setBets] = useState<undefined | BetType[]>(undefined);

    const [addHorseLoading, setAddHorseLoading] = useState(false);
    const [runRaceLoading, setRunRaceLoading] = useState(false);
    const [placeBetLoading, setPlaceBetLoading] = useState(false);

    const contractId = "KT1R1LpgrWpDs6rSAwLDXyyKPtbGB9XBpRQB";
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
        setTrack(storage?.track);

        const horses: HorseType[] = [];
        const horsesInStorage: any = storage?.horses?.valueMap.entries();
        for (let horseDetail of horsesInStorage) {
            const id = horseDetail[0];
            const horseNameDetails = horseDetail[1].valueMap.entries();
            let hName = "";
            for (let horseName of horseNameDetails) {
                hName = horseName[1];
            }
            horses.push({
                horseId: id,
                horseName: hName,
            });
        }
        setHorses(horses);
    };
    const addHorse = async () => {
        Tezos.contract
            .at(contractId)
            .then((contract) => {
                cogoToast.info("Adding horse");
                setAddHorseLoading(true);
                return contract.methods
                    .addHorse(2, "A fresh horse", "426c616168")
                    .send();
            })
            .then((op) => {
                cogoToast.info("Waiting to be confirmed");
                return op.confirmation(3).then(() => op.hash);
            })
            .then((hash) => {
                setAddHorseLoading(false);
                cogoToast.success("Successfully added the horse!");
            })
            .catch((error) => {
                setAddHorseLoading(false);
                console.log(JSON.stringify(error));
                cogoToast.error(
                    `Could not add horse. Error:${JSON.stringify(error)}`
                );
            });
    };
    useEffect(() => {
        // Tezos.setProvider({
        //     rpc: "https://api.tez.ie/rpc/carthagenet",
        //     // signer: new InMemorySigner(
        //     // "edskS6rCh5wPWUd2D2vPRDmxnQppAr1V1e4MksLjQh1YgecFv4eYUaEYkWKFP6nYQJtopN9JT8Ms2vjoCRA4J2cUfRSe84HwZv"
        //     // ),
        // });
        // const interval = setInterval(() => {
        //     setCurrentTime(new Date());
        // }, 1000);
        getTotalBalance();
        getContractDetails();
        // console.log(horses);
        // return () => clearInterval(interval);
    }, []);
    return (
        <div className="content">
            <div className="content__column">
                <div className="content__item">
                    <div className="content__item__title">Track</div>
                    <div className="content__item__content">
                        {track !== undefined ? `${track}` : ""}
                    </div>
                </div>
                <div className="content__item">
                    <div className="content__item__title">Total pool</div>
                    <div className="content__item__content">
                        {totalBalance !== undefined ? `${totalBalance}` : ""}
                    </div>
                </div>
                <div className="content__item">
                    <div className="content__item__title">Time of day</div>
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
                            Horses
                        </div>
                        <div className="content__item__title content__item__title--bets">
                            Bets
                        </div>
                    </div>
                    {horses?.map((horse) => {
                        return (
                            <div className="content__item__content-wrapper">
                                <div className="content__item__content content__item__content--horses">
                                    {horse?.horseName}
                                </div>
                                <div className="content__item__content content__item__content--bets">
                                    {"4"}
                                </div>
                                <div className="content__item__content content__item__content--bets">
                                    {"1"}
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
                        onClick={() => addHorse()}
                    >
                        {addHorseLoading ? (
                            <span className="loadingSpinner"></span>
                        ) : (
                            "Add horse"
                        )}
                    </button>
                </div>
                <div className="content__item">
                    <button className="btn btn--admin">
                        {runRaceLoading ? (
                            <span className="loadingSpinner"></span>
                        ) : (
                            "Run race"
                        )}
                    </button>
                </div>
                <div className="content__item">
                    <button className="btn btn">
                        {placeBetLoading ? (
                            <span className="loadingSpinner"></span>
                        ) : (
                            "Place bet"
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Content;

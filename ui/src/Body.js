import React from 'react';

class Body extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            openPositions: []
        }
    }

    componentDidMount(){
        this.getOpenPositions()
    }

    getOpenPositions(){
        fetch('http://localhost:5000/openpositions')
            .then(res => res.json())
            .then((result) => {
                let positions = []
                for(let pos in result){
                    positions.push(result[pos])
                }
                console.log(positions)
                let map = positions.map((position) =>
                    <li key={position.entry_time}>{position.quantity}&nbsp;<strong>{position.symbol}</strong>&nbsp; at &nbsp;${position.price}</li>
                );
                this.setState({
                    openPositions: map
                })
            })
    }

    render(){
        return (
            <div className='Body'>
                <h3>Open Positions</h3>
                <div className='PositionList'>{this.state.openPositions}</div>
            </div>
        );
    }
}

export default Body;

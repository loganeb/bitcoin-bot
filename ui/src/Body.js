import React from 'react';

class Body extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            openPositions: []
        }
    }

    componentDidMount(){
        var openPositions = this.getOpenPositions()
        this.setState({
            openPositions: openPositions
        })
    }

    getOpenPositions(){
        var list = [
            {symbol: 'ETH', quantity: 0.0003, price: 30000.00}
        ]
        return list.map((position) =>
            <li>{position.quantity}&nbsp;<strong>{position.symbol}</strong>&nbsp; at &nbsp;${position.price}</li>
        );
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

import React from 'react';
import ReactDOM from 'react-dom';
import PlayerGames from './PlayerGames'
import AvailableGames from './AvailableGames'
import Websocket from 'react-websocket'
import $ from 'jquery'

class LobbyBase extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            player_game_list: [],
            available_game_list: []
        }

        // bind button click
        this.sendSocketMessage = this.sendSocketMessage.bind(this);
    }

    getPlayerGames(){
        this.serverRequest = $.get('http://localhost:8080/player-games/?format=json', function (result) {
           this.setState({
            player_game_list: result,
             })
        }.bind(this))
    }

    getAvailableGames(){
        this.serverRequest = $.get('http://localhost:8080/available-games/?format=json', function (result) {
           this.setState({
            available_game_list: result
             })
        }.bind(this))
    }

    componentDidMount() {
       this.getPlayerGames()
       this.getAvailableGames()
        
        
    }

    componentWillUnmount() {
        this.serverRequest.abort();
    }

    handleData(data) {
        //receives messages from the connected websocket
        let result = JSON.parse(data)
        // new games, so get an updated list of this player's game
        this.getPlayerGames()
        // we've received an updated list of available games
        this.setState({available_game_list: result})
    }

    sendSocketMessage(message){
        // sends message to channels back-end
       const socket = this.refs.socket
       socket.state.ws.send(JSON.stringify(message))
    }

    render() {
        return (

            <div className="row">
                <div className="col-lg-4">
                    <PlayerGames player={this.props.current_user} game_list={this.state.player_game_list}
                                 sendSocketMessage={this.sendSocketMessage} />
                </div>
                 <div className="col-lg-4">
                     <AvailableGames player={this.props.current_user} game_list={this.state.available_game_list}
                                     sendSocketMessage={this.sendSocketMessage} />
                </div>
                <Websocket ref="socket" url={this.props.socket}
                    onMessage={this.handleData.bind(this)} reconnect={true}/>

            </div>

        )
    }
}

LobbyBase.defaultProps = {

};

LobbyBase.propTypes = {
    socket: React.PropTypes.string
};

export default LobbyBase;

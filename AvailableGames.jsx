import React from 'react'

class AvailableGames extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            game_list: this.props.game_list
        }

     this.renderGameList = this.renderGameList.bind(this);

    }

    componentWillReceiveProps(newProp) {
        this.setState({ game_list: newProp.game_list })
    }

    renderGameList() {
        // clear out games owned by this player
        let player_removed = this.props.game_list.filter(function(game) {
            return game.creator.id !== this.props.player.id
        }, this);
        
        
        if (player_removed.length > 0) {
            return player_removed.map(function (game) {
                    return <li key={game.id} className="list-group-item">
                        <span className="badge pull-left">{game.id}</span>&nbsp; &nbsp;
                        <span>{game.creator.username} vs???</span>
                        <a className="btn btn-sm btn-primary pull-right" href={"/game/"+game.id+"/"}>Play</a>
                    </li>
            }, this)

        } else {
            return ("No Available Games")
        }
    }

    render() {
        return (
            <div>
                <div className="panel panel-primary">
                    <div className="panel-heading">
                        <span>Available Games</span>
                    </div>
                    <div className="panel-body">
                        <div>
                            <ul className="list-group games-list">
                                {this.renderGameList() }
                            </ul>
                        </div>
                    </div>
                </div>

            </div>
        )
    }
}

AvailableGames.defaultProps = {

};

AvailableGames.propTypes = {
    game_list: React.PropTypes.array,
    player: React.PropTypes.object

};


export default AvailableGames


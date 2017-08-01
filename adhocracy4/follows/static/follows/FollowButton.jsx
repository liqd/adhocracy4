var api = require('../../../static/api')
var django = require('django')
var React = require('react')

class FollowButton extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      followed: undefined,
      follows: 0
    }
  }
  toggleFollow () {
    api.follow.change({ enabled: !this.state.followed }, this.props.project)
       .done((follow) => {
         this.setState({
           followed: follow.enabled,
           follows: follow.follows
         })
       })
  }
  componentDidMount () {
    api.follow.get(this.props.project)
       .done((follow) => {
         this.setState({
           followed: follow.enabled,
           follows: follow.follows
         })
       })
       .fail((response) => {
         if (response.status === 404) {
           this.setState({
             followed: false
           })
         }
       })
  }
  render () {
    return (
      <span className="btngroup btngroup-gray">
        <button className="btn btn-sm btn-dark btn-primary" type="button" onClick={this.toggleFollow.bind(this)}>
          <i className={this.state.followed ? 'fa fa-star' : 'fa fa-star-o'} aria-hidden="true" />
          &nbsp;{this.state.followed ? django.gettext('Unfollow') : django.gettext('Follow')}
        </button>
        <span className="btn btn-sm btn-dark btn-primary">{this.state.follows}</span>
      </span>
    )
  }
}

module.exports = FollowButton

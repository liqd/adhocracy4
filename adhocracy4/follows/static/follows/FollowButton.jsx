var api = require('adhocracy4').api
var django = require('django')
var React = require('react')

var FollowButton = React.createClass({
  getInitialState: function () {
    return {
      followed: undefined,
      follows: 0
    }
  },
  toggleFollow: function () {
    api.follow.change({ enabled: !this.state.followed }, this.props.project)
       .done((follow) => {
         this.setState({
           followed: follow.enabled,
           follows: follow.follows
         })
       })
  },
  componentDidMount: function () {
    api.follow.get(this.props.project)
       .done((follow) => {
         this.setState({
           followed: follow.enabled,
           follows: follow.follows
         })
       })
       .fail((response) => {
         response.status === 404
         this.setState({
           followed: false
         })
       })
  },
  render: function () {
    return (
      <span className="btngroup btngroup-gray">
        <button className="btn btn-sm btn-dark btn-primary" type="button" onClick={this.toggleFollow}>
          <i className={this.state.followed ? 'fa fa-star' : 'fa fa-star-o'} aria-hidden="true" />
          &nbsp;{this.state.followed ? django.gettext('Unfollow') : django.gettext('Follow')}
        </button>
        <span className="btn btn-sm btn-dark btn-primary">{this.state.follows}</span>
      </span>
    )
  }
})

module.exports = FollowButton

var api = require('../../../contrib/static/js/api')
var config = require('../../../contrib/static/js/config')

var React = require('react')
var ReactDOM = require('react-dom')
var h = require('react-hyperscript')
var classnames = require('classnames')

var RatingBox = React.createClass({
  handleRatingCreate: function (number) {
    api.rating.add({
      object_pk: this.props.objectId,
      content_type: this.props.contentType,
      value: number
    }).done(function (data) {
      this.setState({
        positiveRatings: data.meta_info.positive_ratings_on_same_object,
        negativeRatings: data.meta_info.negative_ratings_on_same_object,
        userRating: data.meta_info.user_rating_on_same_object_value,
        userHasRatingd: true,
        userRatingId: data.id
      })
    }.bind(this))
  },
  handleRatingModify: function (number, id) {
    api.rating.change({value: number}, id)
      .done(function (data) {
        this.setState({
          positiveRatings: data.meta_info.positive_ratings_on_same_object,
          negativeRatings: data.meta_info.negative_ratings_on_same_object,
          userRating: data.meta_info.user_rating_on_same_object_value
        })
      }.bind(this))
  },
  updateUserRating: function (data) {
    this.state.ratings[this.state.userRatingIndex] = data
  },
  ratingUp: function (e) {
    e.preventDefault()
    if (this.props.authenticatedAs === null) {
      window.location.href = config.loginUrl
      return
    }
    if (this.props.isReadOnly) {
      return
    }
    if (this.state.userHasRatingd) {
      var number
      if (this.state.userRating === 1) {
        number = 0
      } else {
        number = 1
      }
      this.handleRatingModify(number, this.state.userRatingId)
    } else {
      this.handleRatingCreate(1)
    }
  },
  ratingDown: function (e) {
    e.preventDefault()
    if (this.props.authenticatedAs === null) {
      window.location.href = config.loginUrl
      return
    }
    if (this.props.isReadOnly) {
      return
    }
    if (this.state.userHasRatingd) {
      var number
      if (this.state.userRating === -1) {
        number = 0
      } else {
        number = -1
      }
      this.handleRatingModify(number, this.state.userRatingId)
    } else {
      this.handleRatingCreate(-1)
    }
  },
  getInitialState: function () {
    return {
      positiveRatings: this.props.positiveRatings,
      negativeRatings: this.props.negativeRatings,
      userHasRatingd: this.props.userRating !== null,
      userRating: this.props.userRating,
      userRatingId: this.props.userRatingId
    }
  },
  componentDidMount: function () {
    this.getInitialState()
  },
  render: function () {
    let getRatingClasses = ratingType => {
      let valueForRatingType = ratingType === 'up' ? 1 : -1
      return classnames(`rating-button rating-${ratingType}`, {
        'is-read-only': this.props.isReadOnly,
        'is-selected': this.state.userRating === valueForRatingType
      })
    }

    return (
      <ul className="ul nav navbar-nav rating-bar">
        <li className="entry">
          <button className={getRatingClasses('up')} onClick={this.ratingUp}>
            <i className="fa fa-chevron-up" />
            {this.state.positiveRatings}
          </button>
        </li>
        <li className="entry">
          <button className={getRatingClasses('down')} onClick={this.ratingDown}>
            <i className="fa fa-chevron-down" />
            {this.state.negativeRatings}
          </button>
        </li>
      </ul>
    )
  }
})

module.exports.RatingBox = RatingBox

module.exports.renderRatings = function (mountpoint, props) {
  ReactDOM.render(h(RatingBox, props), document.getElementById(mountpoint))
}

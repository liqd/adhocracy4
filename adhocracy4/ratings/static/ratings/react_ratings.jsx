var api = require('../../../static/api')
var config = require('../../../static/config')

var React = require('react')
var ReactDOM = require('react-dom')
var classnames = require('classnames')

var RatingBox = React.createClass({
  handleRatingCreate: function (number) {
    api.rating.add({
      urlReplaces: {
        objectPk: this.props.objectId,
        contentTypeId: this.props.contentType,
      },
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
    api.rating.change({
      urlReplaces: {
        objectPk: this.props.objectId,
        contentTypeId: this.props.contentType,
      },
      value: number
    }, id)
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
        'is-selected': this.state.userRating === valueForRatingType
      })
    }

    return (
      <div className="rating">
        <button
          className={getRatingClasses('up')}
          disabled={this.props.isReadOnly}
          onClick={this.ratingUp}>
          <i className="fa fa-chevron-up" aria-hidden="true" />
          {this.state.positiveRatings}
        </button>
        <button
          className={getRatingClasses('down')}
          disabled={this.props.isReadOnly}
          onClick={this.ratingDown}>
          <i className="fa fa-chevron-down" aria-hidden="true" />
          {this.state.negativeRatings}
        </button>
      </div>
    )
  }
})

module.exports.RatingBox = RatingBox

module.exports.renderRatings = function (mountpoint) {
  let el = document.getElementById(mountpoint)
  let props = JSON.parse(el.getAttribute('data-attributes'))
  ReactDOM.render(<RatingBox {...props} />, el)
}

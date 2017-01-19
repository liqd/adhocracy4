var ReactComments = require('adhocracy4').comments
var ReactRatings = require('adhocracy4').ratings
var dropdown = require('./dropdown');

// make jquery available for non-webpack js
window.jQuery = window.$ = require('jquery');

module.exports = {
  'renderComment': ReactComments.renderComment,
  'renderRatings': ReactRatings.renderRatings
}

var ReactComments = require('adhocracy4').comments
var ReactRatings = require('adhocracy4').ratings

// make jquery available for non-webpack js
window.jQuery = window.$ = require('jquery');

var dropdown = require('bootstrap/js/src/dropdown.js');

module.exports = {
  'renderComment': ReactComments.renderComment,
  'renderRatings': ReactRatings.renderRatings
}

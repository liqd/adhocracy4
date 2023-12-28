import 'bootstrap' // load bootstrap components
import 'django'
import 'select2' // used to select projects in containers
import 'shariff'
import 'slick-carousel'

import '../../apps/actions/assets/timestamps.js'
import '../../apps/moderatorremark/assets/idea_remarks.js'
import '../../apps/newsletters/assets/dynamic_fields.js'

// map search function
import 'adhocracy4/adhocracy4/maps/static/a4maps/a4maps_address.js'

// expose react components
import {
  commentsAsync as ReactCommentsAsync,
  follows as ReactFollows,
  ratings as ReactRatings,
  reports as ReactReports,
  widget as ReactWidget
} from 'adhocracy4'

import * as ReactMapTeaser from '../../apps/plans/assets/react_map_teaser.jsx'

function init () {
  const shariffs = $('.shariff')
  if (shariffs.length > 0) {
    /* eslint-disable no-new */
    new window.Shariff(shariffs, {
      services: '[&quot;twitter&quot;,&quot;facebook&quot;,&quot;info&quot;]',
      infoUrl: '/shariff'
    })
  }

  ReactWidget.initialise('a4', 'comment_async', ReactCommentsAsync.renderComment)
  ReactWidget.initialise('a4', 'follows', ReactFollows.renderFollow)
  ReactWidget.initialise('a4', 'ratings', ReactRatings.renderRatings)
  ReactWidget.initialise('a4', 'reports', ReactReports.renderReports)

  ReactWidget.initialise('mb', 'mapTeaser', ReactMapTeaser.renderFilter)

  $('.timeline-carousel__item').slick({
    initialSlide: parseInt($('#timeline-carousel').attr('data-initial-slide')),
    focusOnSelect: false,
    centerMode: true,
    dots: false,
    arrows: true,
    centerPadding: 30,
    mobileFirst: true,
    infinite: false,
    variableWidth: true,
    slidesToShow: 1,
    slidesToScroll: 1
  })

  if ($.fn.select2) {
    $('.js-select2').select2()
    $('.select2__no-search').select2({
      minimumResultsForSearch: -1
    })
  }
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)

// This function is overwritten with custom behavior in embed.js.
export function getCurrentPath () {
  return location.pathname
}

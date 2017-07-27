const moment = require('moment')
const $ = require('jquery')

$(function () {
  const $times = $('time.relative')

  $times.each((i, e) => {
    let datetime = moment($(e).attr('datetime'))

    if (datetime.isAfter(moment().subtract(7, 'days'))) {
      e.textContent = datetime.fromNow()
    }
  })
})

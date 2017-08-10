const timeago = require('timeago.js')
const $ = require('jquery')

$(function () {
  const $times = $('time.relative')

  $times.each((i, e) => {
    const sevenDays = 60 * 60 * 24 * 7 * 1000
    let datetime = new Date($(e).attr('datetime'))
    let relativeTime = timeago().format(datetime)

    if ((new Date() - datetime) < sevenDays) {
      e.textContent = relativeTime
    }
  })
})

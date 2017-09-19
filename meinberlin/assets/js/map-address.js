var example = { 'type': 'FeatureCollection', 'count': 6, 'next': null, 'previous': null, 'features': [ { 'type': 'Feature', 'geometry': { 'type': 'Point', 'coordinates': [ 13.47477240708322, 52.5014732657076 ] }, 'properties': { 'strname': 'Hauptstraße', 'hsnr': '3', 'plz': '10317', 'bezirk_name': 'Lichtenberg' } }, { 'type': 'Feature', 'geometry': { 'type': 'Point', 'coordinates': [ 13.359589931630357, 52.49008194823388 ] }, 'properties': { 'strname': 'Hauptstraße', 'hsnr': '3', 'plz': '10827', 'bezirk_name': 'Tempelhof-Schöneberg' } }, { 'type': 'Feature', 'geometry': { 'type': 'Point', 'coordinates': [ 13.431013026636759, 52.60269551910352 ] }, 'properties': { 'strname': 'Hauptstraße', 'hsnr': '3', 'plz': '13127', 'bezirk_name': 'Pankow' } }, { 'type': 'Feature', 'geometry': { 'type': 'Point', 'coordinates': [ 13.366162828729282, 52.584292375802704 ] }, 'properties': { 'strname': 'Hauptstraße', 'hsnr': '3', 'plz': '13158', 'bezirk_name': 'Pankow' } }, { 'type': 'Feature', 'geometry': { 'type': 'Point', 'coordinates': [ 13.386506977652546, 52.61771816185583 ] }, 'properties': { 'strname': 'Hauptstraße', 'hsnr': '3', 'plz': '13159', 'bezirk_name': 'Pankow' } }, { 'type': 'Feature', 'geometry': { 'type': 'Point', 'coordinates': [ 13.143751928723624, 52.52922828118691 ] }, 'properties': { 'strname': 'Hauptstraße', 'hsnr': '3', 'plz': '13591', 'bezirk_name': 'Spandau' } } ] }

var mockAjax = function (config) {
  setTimeout(function () {
    config.success(example)
  }, 400)
}

var setBusy = function ($group, busy) {
  $group.attr('aria-busy', busy)
  $group.find('input').attr('disabled', busy)
  $group.find('button').attr('disabled', busy)
  if (busy) {
    $group.find('.fa')
      .addClass('fa-spinner fa-pulse')
      .removeClass('fa-search')
  } else {
    $group.find('.fa')
      .addClass('fa-search')
      .removeClass('fa-spinner fa-pulse')
  }
}

var getPoints = function (address, cb) {
  // TODO: enable once API is available
  // $.ajax('/geocoding', {
  mockAjax({
    data: {address: address},
    success: function (geojson) {
      // TODO: filter by polygon
      cb(geojson.features)
    },
    error: function () {
      var points = []
      cb(points)
    }
  })
}

var init = function () {
  var $ = window.jQuery

  $('[data-map="address"]').each(function (i, e) {
    var $group = $(e)
    var $input = $('#id_' + $group.data('name'))

    var onSubmit = function (event) {
      event.preventDefault()
      setBusy($group, true)
      var address = $group.find('input').val()
      getPoints(address, function (points) {
        setBusy($group, false)
        // TODO: show error if no results
        // TODO: allow user to pick if more than one result
        $input.val(JSON.stringify(points[0])).change()
      })
    }

    // simulate a nested form
    $group.find('button').click(onSubmit)
    $group.find('input').on('change', onSubmit)
    $group.find('input').on('keydown', function (event) {
      if (event.keyCode === 13) {
        onSubmit(event)
      }
    })
  })
}

window.jQuery(init)
window.jQuery(document).on('a4.embed.ready', init)

const $ = require('jquery')
const a4api = require('adhocracy4').api

$(function () {
  const dropdown = $('#idea-remark__dropdown')
  const attributes = dropdown.data('attributes')
  if (typeof attributes !== 'undefined') {
    var objectPk = attributes.item_object_id
    var contentTypeId = attributes.item_content_type
    var remarkId = attributes.id
    var remarkVal = attributes.remark
  }

  if (remarkId) {
    $('#id_remark').val(remarkVal)
  }

  $('#idea-remark__form').submit(function (e) {
    e.preventDefault()
    const $input = $('#id_remark')
    const newVal = $input.val()

    if (remarkVal !== newVal) {
      const data = {
        urlReplaces: {
          objectPk: objectPk,
          contentTypeId: contentTypeId
        },
        remark: newVal
      }

      var response
      if (remarkId) {
        response = a4api.moderatorremark.change(data, remarkId)
      } else {
        response = a4api.moderatorremark.add(data)
      }

      response.done(remark => {
        remarkId = remark.id
        remarkVal = remark.remark
        $('.dropdown.show .dropdown-toggle').dropdown('toggle')
        if (remarkVal) {
          dropdown.find('.idea-remark__btn__notify').show()
        } else {
          dropdown.find('.idea-remark__btn__notify').hide()
        }
      })
    } else {
      $('.dropdown.show .dropdown-toggle').dropdown('toggle')
    }
  })
})

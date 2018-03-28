const $ = require('jquery')
const a4api = require('adhocracy4').api

$(function () {
  const $btn = $('#idea--popover__btn')

  const attributes = $btn.data('attributes')
  const objectPk = attributes['item_object_id']
  const contentTypeId = attributes['item_content_type']

  var remarkId = attributes['id']
  var remarkVal = attributes['remark']

  $btn.popover()

  $btn.on('hide.bs.popover', function () {
    const $input = $('#idea--popover__input')
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
      })
    }
  })

  $('#idea--popover__btn').on('inserted.bs.popover', function () {
    const $input = $('#idea--popover__input')
    $input.val(remarkVal)
  })
})

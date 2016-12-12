var $ = require('jquery')
var cookie = require('js-cookie')

$(function () {
  $.ajaxSetup({
    headers: { 'X-CSRFToken': cookie.get('csrftoken') }
  })
})

var baseURL = '/api/'

var api = (function () {
  var urls = {
    comment: baseURL + 'comments/',
    rating: baseURL + 'ratings/',
    report: baseURL + 'reports/',
    document: baseURL + 'documents/',
    follow: baseURL + 'follows/'
  }

  function _sendRequest (endpoint, id, options, data, contentType) {
    var $body = $('body')
    var url = urls[endpoint]
    if (typeof id === 'object') {
      // there's no id, switch parameters
      data = options
      options = id
    } else if (typeof id === 'number' || typeof id === 'string') {
      url = url + id + '/'
    }
    var defaultParams = {
      url: url,
      dataType: 'json',
      data: data,
      error: function (xhr, status, err) {
        console.error(url, status, err.toString())
      },
      complete: function () {
        $body.removeClass('loading')
      }
    }
    var params = $.extend(defaultParams, options)

    if (typeof params.data !== 'undefined') {
      if (params.type === 'PUT' || params.type === 'POST' ||
          params.type === 'PATCH'
      ) {
        params.contentType = 'application/json; charset=utf-8'
        params.data = JSON.stringify(params.data)
      }
    }

    $body.addClass('loading')
    return $.ajax(params)
  }

  return {
    comments: {
      get: function (data) {
        return _sendRequest('comment', {
          cache: false,
          type: 'GET'
        }, data)
      },

      add: function (data) {
        return _sendRequest('comment', {
          type: 'POST'
        }, data)
      },

      change: function (data, id) {
        return _sendRequest('comment', id, {
          type: 'PATCH'
        }, data)
      },

      delete: function (id) {
        return _sendRequest('comment', id, {
          type: 'DELETE'
        })
      }
    },
    rating: {
      add: function (data) {
        return _sendRequest('rating', {
          type: 'POST'
        }, data)
      },
      change: function (data, id) {
        return _sendRequest('rating', id, {
          type: 'PATCH'
        }, data)
      }
    },
    report: {
      submit: function (data) {
        return _sendRequest('report', {
          type: 'POST'
        }, data)
      }
    },
    document: {
      add: function (data) {
        return _sendRequest('document', {
          type: 'POST'
        }, data)
      },
      change: function (data, id) {
        return _sendRequest('document', id, {
          type: 'PUT'
        }, data)
      }
    },
    follow: {
      get: function (slug) {
        return _sendRequest('follow', slug, {
          type: 'GET'
        }, {})
      },
      change: function (data, slug) {
        return _sendRequest('follow', slug, {
          type: 'PUT'
        }, data)
      }
    }
  }
}())
module.exports = api

var $ = require('jquery');

$(document).ready(function() {
  $('.dropdown').each(function(index, el) {
      var $el = $(el);
      var $toggle = $el.find('.dropdown-toggle');
      var $menu = $el.find('.dropdown-menu');

      var id = 'dropdown-toggle-' + Math.random();

      var setShow = function(isShow) {
          if (isShow) {
              $el.addClass('is-show');
              $menu.show();
              $toggle.attr('aria-expanded', 'false');
          } else {
              $el.removeClass('is-show');
              $menu.hide();
              $toggle.attr('aria-expanded', 'false');
          }
      };

      $menu.attr('aria-labelledby', id);

      $toggle
          .attr('id', id)
          .attr('aria-haspopup', 'true')
          .attr('aria-expanded', 'false')
          .click(function() {
              setShow(!$el.hasClass('is-show'));
          });

      $el.on('focusout', function() {
          window.setTimeout(function() {
              if (!$.contains(el, document.activeElement)) {
                  setShow(false);
              }
          });
      });

      setShow(false);
  });
});

(function($) {

  'use strict';

  $.cmdbox = {
    init: function () {
      $.fn.slugify = function () {
        var str = $(this).val()
        var slug = $.cmdbox.slug(str);
        $(this).val(slug);
      };

      $.fn.renderDialog = function (title, message) {
        $(this).find(".modal-title, .modal-body").empty();
        $(".modal-title", this).text(title);
        if ($.isArray(message)) {
          $.each(message, function (index, value) {
            $("</p>").text(value).appendTo(".modal-body", this);
          });
        }
        else {
          $("</p>").text(message).appendTo(".modal-body", this);
        }
        $(this).modal();
      };

      $("[data-toggle='tooltip']").tooltip();
    },

    getCSRF: function () {
      return $("meta[name='csrf']").attr("content");
    },

    slug: function (str) {
      str = str.replace(/^\s+|\s+$/g, ''); // trim
      str = str.toLowerCase();

      // remove accents, swap ñ for n, etc
      var from = "ãàáäâẽèéëêìíïîõòóöôùúüûñç·/_,:;";
      var to   = "aaaaaeeeeeiiiiooooouuuunc------";
      for (var i=0, l=from.length ; i<l ; i++) {
        str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
      }

      str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
        .replace(/\s+/g, '-') // collapse whitespace and replace by -
        .replace(/-+/g, '-'); // collapse dashes

      return str;
    },

    loading: function () {
      $(".loading").show();
      $("body").css("overflow", "hidden");
    },

    stopLoading: function () {
      $(".loading").hide();
      $("body").css("overflow", "scroll");
    },

    isElementInViewport: function (el) {
      /* http://stackoverflow.com/questions/123999/how-to-tell-if-a-dom-element-is-visible-in-the-current-viewport/7557433#7557433 */

      if (typeof jQuery === "function" && el instanceof jQuery) {
          el = el[0];
      }

      var rect = el.getBoundingClientRect();

      return (
          rect.top >= 0 &&
          rect.left >= 0 &&
          rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
          rect.right <= (window.innerWidth || document.documentElement.clientWidth)
      );
    },

    alert: function (title, message) {
      $("#modal-alert").renderDialog(title, message);
    },

    confirm: function (title, message, confirmCallback, cancelCallback) {
      confirmCallback = confirmCallback || function () {};
      cancelCallback = cancelCallback || function () {};

      $("#modal-confirm-action").unbind("hide.bs.modal");
      $("#modal-confirm-action").on("hide.bs.modal", cancelCallback);

      var confirmCallbackWrapper = function () {
        $("#modal-confirm-action").unbind("hide.bs.modal");
        $("#modal-confirm-action").modal("hide");
        confirmCallback();
      };

      $("#modal-confirm-action .js-confirm-action").unbind("click").bind("click", confirmCallbackWrapper);
      $("#modal-confirm-action").renderDialog(title, message);
    }

  };

})(jQuery);

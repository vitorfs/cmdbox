(function($) {

  'use strict';

  $.cmdbox = {
    init: function () {

      /* Slugify helper function */
      $.fn.slugify = function () {
        var str = $(this).val()
        var slug = $.cmdbox.slug(str);
        $(this).val(slug);
      };

      /* Bootstrap modal renderer */
      $.fn.renderDialog = function (title, message) {
        $(this).find(".modal-title, .modal-body").empty();
        $(".modal-title", this).html(title);
        if ($.isArray(message)) {
          $.each(message, function (index, value) {
            $("</p>").html(value).appendTo(".modal-body", this);
          });
        }
        else {
          $("</p>").html(message).appendTo(".modal-body", this);
        }
        $(this).modal();
      };

      /* Add stripped lines */
      $.fn.stripTable = function () {
        $("tbody tr:visible", this).each(function (index) {
          if (index % 2 == 0) {
            $(this).removeClass("odd").addClass("even");
          }
          else {
            $(this).removeClass("even").addClass("odd");
          }
        });
      };

      /* Activate tooltip plugin */
      $("[data-toggle='tooltip']").tooltip();

      /* CSRF protection for AJAX request */
      var csrfSafeMethod = function (method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
      };

      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
          $.cmdbox.loading();
          var csrftoken = Cookies.get("csrftoken");
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
        },
        complete: function () {
          $.cmdbox.stopLoading();
        }
      });

      /* Async Form Setup */
      $.fn.getCallbackFunction = function (attrName) {
        var formId = $(this).attr("id");
        var functionName = $(this).attr(attrName);
        if (functionName !== undefined) {
          var callbackFunction = "#" + formId + ":" + functionName;
          return $.cmdbox.fn[callbackFunction];
        }
      };

      $("body").on("submit", "[data-async='true']", function () {
        var form = $(this);

        $.ajax({
          url: $(form).attr("action"),
          type: $(form).attr("method"),
          data: $(form).serialize(),
          beforeSend: function(xhr, settings) {
            var csrftoken = Cookies.get("csrftoken");
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
            var callback = $(form).getCallbackFunction("data-before-send");
            if (callback !== undefined) {
              callback();
            }
            $.cmdbox.loading();
          },
          success: function (data) {
            var callback = $(form).getCallbackFunction("data-success");
            if (callback !== undefined) {
              callback(data);
            }
          }
        });
        return false;
      });

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
    },

    fn: new Array(),

    ENTER_KEY: 13,
    ESCAPE_KEY: 27

  };

})(jQuery);

$(function () {

  /***************************************************************************/
  /* Functions                                                               */
  /***************************************************************************/

  var loadFileForm = function () {
    var url = $(this).attr("data-url");
    var folder_id = $(this).attr("data-folder-id");
    $.ajax({
      url: url,
      type: 'get',
      cache: false,
      beforeSend: function () {
        $.cmdbox.loading();
      },
      success: function (data) {
        if (folder_id === undefined) {
          $("#table-files tbody").prepend(data.form);
          $("#form-add-file").closest("td").css("padding-left", "26px");
        }
        else {
          var parent = $("#table-files tbody tr[data-id='" + folder_id + "']");
          var depth = parseInt($(parent).attr("data-depth"));
          var padding = (26 + ((depth + 1) * 24));
          $(parent).after(data.form);
          $("#form-add-file").closest("td").css("padding-left", padding + "px");
        }
        $("#id_add_file-name").focus();
        $("#id_add_file-name").select();
      },
      complete: function () {
        $.cmdbox.stopLoading();
      }
    });
  };

  var saveFile = function () {
    /*
      Serialize the form CreateFileForm and post it to the defined reversed url.
      Used both for the views `add_file` and `add_children_file`.
      Before sending the form, display the application loading state.
      On success, check if the form was valid and redraw the file tree and focus on the recently added file.
      If the recently added file is visible in the viewport, add blue background (css .info class) and remove it
      after 0.5 seconds. If the recently added wasn't visible in the viewport, scroll to the element first and then
      apply the css class.
      If the form wasn't valid, replace the form with the validated form displaying the errors.
      On complete, reset the application loading state.
    */
    $.ajax({
      url: $("#form-add-file").attr("action"),
      data: $("#form-add-file").serialize(),
      type: 'post',
      beforeSend: function () {
        $.cmdbox.loading();
      },
      success: function (data) {
        if (data.is_valid) {
          $("#table-files tbody").html(data.html);
          var row = $("#table-files tbody tr[data-id='" + data.file + "']");
          $(row).addClass("info");
          var removeFeaturedRow = function () {
            setTimeout(function () {
              $(row).removeClass("info");
            }, 500)
          };

          if ($.cmdbox.isElementInViewport(row)) {
            removeFeaturedRow();
          }
          else {
            var options = {
              scrollTop: $(row).offset().top
            };
            var duration = 500;
            var callback = removeFeaturedRow;
            $("html, body").animate(options, duration, callback);
          }

        }
        else {
          $("#form-add-file").closest("tr").replaceWith(data.form);
        }
      },
      complete: function () {
        $.cmdbox.stopLoading();
      }
    });
    return false;
  };

  var deleteFile = function () {
    var btn = $(this);
    $.ajax({
      url: $(btn).attr("data-url"),
      data: {
        'csrfmiddlewaretoken': $.cmdbox.getCSRF()
      },
      type: 'post',
      beforeSend: function () {
        $.cmdbox.loading();
      },
      success: function (data) {
        $("#table-files tbody").html(data.html);
        $(".items-count").text(data.itemsCount);
      },
      complete: function () {
        $.cmdbox.stopLoading();
      }
    });
  };


  /***************************************************************************/
  /* Binding                                                                 */
  /***************************************************************************/

  /* Add files/folders */
  $("main").on("click", ".js-add-file", loadFileForm);
  $("#table-files").on("blur", "#id_add_file-name", saveFile);
  $("#table-files").on("submit", "#form-add-file", saveFile);

  /* Delete files/folders */
  $("main").on("click", ".js-delete-file", deleteFile);

});

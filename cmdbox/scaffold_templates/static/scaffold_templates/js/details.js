$(function () {

  /***************************************************************************/
  /* Functions                                                               */
  /***************************************************************************/

  var loadAddFileForm = function () {
    var url = $(this).attr("data-url");
    var folder_id = $(this).attr("data-folder-id");
    var has_parent = folder_id !== undefined;

    var depth = 0;
    if (has_parent) {
      var parent = $(this).closest("tr");
      var parent_depth = parseInt($(parent).attr("data-depth"));
      depth = parent_depth + 1;
    }

    $.ajax({
      url: url,
      type: 'get',
      data: {
        'depth': depth
      },
      cache: false,
      success: function (data) {
        if (has_parent) {
          $(parent).after(data.form);
        }
        else {
          $("#table-files tbody").prepend(data.form);
        }
        $("#id_name").focus();
        $("#id_name").select();
      }
    });
  };

  var loadRenameFileForm = function () {
    var row = $(this).closest("tr");
    var depth = $(row).attr("data-depth");
    var url = $(this).attr("data-url");
    $.ajax({
      url: url,
      type: 'get',
      data: {
        'depth': depth
      },
      cache: false,
      success: function (data) {
        $(row).replaceWith(data.form);
        $("#id_name").focus();
        $("#id_name").select();
      }
    });
  };

  var addFeaturedClass = function (id, children) {
    children = children || new Array();
    var row = $("#table-files tbody tr[data-id='" + id + "']");
    $(row).addClass("info");
    $(children).each(function () {
      $(this).addClass("info");
    });
    var removeFeaturedClass = function () {
      setTimeout(function () {
        $(row).removeClass("info");
        $(children).each(function () {
          $(this).removeClass("info");
        });
      }, 500)
    };

    if ($.cmdbox.isElementInViewport(row)) {
      removeFeaturedClass();
    }
    else {
      var options = {
        scrollTop: $(row).offset().top
      };
      var duration = 500;
      var callback = removeFeaturedClass;
      $("html, body").animate(options, duration, callback);
    }
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
      The script returns false to avoid the #form-file to be actually submitted.
    */
    $.ajax({
      url: $("#form-file").attr("action"),
      data: $("#form-file").serialize(),
      type: 'post',
      success: function (data) {
        if (data.is_valid) {
          $("#table-files tbody").html(data.html);
          $(".items-count").text(data.itemsCount);
          addFeaturedClass(data.file);
        }
        else {
          $("#form-file").closest("tr").replaceWith(data.form);
        }
      }
    });
    return false;
  };

  var deleteFile = function () {
    var btn = $(this);
    var title = $(this).attr("data-confirm-title");
    var message = $(this).attr("data-confirm-message");

    $.cmdbox.confirm(title, message, function () {
      $.ajax({
        url: $(btn).attr("data-url"),
        type: 'post',
        success: function (data) {
          $("#table-files tbody").html(data.html);
          $(".items-count").text(data.itemsCount);
        }
      });
    });

  };

  var duplicateFile = function () {
    var url = $(this).attr("data-url");
    $.ajax({
      url: url,
      type: 'post',
      success: function (data) {
        $("#table-files tbody").html(data.html);
        $(".items-count").text(data.itemsCount);

        var collectChildrends = false;
        var parentDepth = -1;
        var children = new Array();
        $("table tbody tr").each(function () {
          if (collectChildrends) {
            var depth = parseInt($(this).attr("data-depth"));
            if (depth === parentDepth) {
              return false;
            }
            else {
              children.push($(this));
            }
          }
          if ($(this).attr("data-id") === data.file.toString()) {
            parentDepth = parseInt($(this).attr("data-depth"));
            collectChildrends = true;
          }
        });

        console.log(children);
        addFeaturedClass(data.file, children);

      }
    });
  };


  /***************************************************************************/
  /* Binding                                                                 */
  /***************************************************************************/

  /* Add files/folders */
  $("main").on("click", ".js-add-file", loadAddFileForm);
  $("main").on("click", ".js-rename-file", loadRenameFileForm);
  //$("#table-files").on("blur", "#id_name", saveFile);
  $("#table-files").on("submit", "#form-file", saveFile);

  /* Delete files/folders */
  $("main").on("click", ".js-delete-file", deleteFile);

  /* Duplicate files/folders */
  $("main").on("click", ".js-duplicate-file", duplicateFile);

});

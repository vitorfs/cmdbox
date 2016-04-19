$(function () {

  /***************************************************************************/
  /* Support Functions (Table Helpers)                                       */
  /***************************************************************************/

  var collectChildren = function (id) {
    var file = $("tr[data-id='" + id + "']");
    var children = new Array();

    if ($(file).attr("data-type") === "folder") {
      var collect = false;
      var parentDepth = -1;
      $("#table-files tbody tr").each(function () {
        if (collect) {
          var depth = parseInt($(this).attr("data-depth"));
          if (depth <= parentDepth) {
            collect = false;
          }
          else {
            children.push($(this));
          }
          return collect;
        }
        if ($(this).attr("data-id") === id.toString()) {
          parentDepth = parseInt($(this).attr("data-depth"));
          collect = true;
        }
      });
    }

    return children;
  };

  var addFeaturedClass = function (featuredClass, id, children, removeClassCallback) {
    children = children || new Array();
    removeClassCallback = removeClassCallback || function () {};

    var row = $("#table-files tbody tr[data-id='" + id + "']");
    $(row).addClass(featuredClass);
    $(children).each(function () {
      $(this).addClass(featuredClass);
    });
    var removeFeaturedClass = function () {
      setTimeout(function () {
        $(row).removeClass(featuredClass);
        $(children).each(function () {
          $(this).removeClass(featuredClass);
        });
        removeClassCallback();
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

  var toggleFolder = function () {
    var folder = $(this).closest("tr");
    var id = $(folder).attr("data-id");
    var children = collectChildren(id);
    if ($(folder).attr("data-expanded") === "true") {
      $(".folder-expand-icon", folder).removeClass("glyphicon-triangle-bottom").addClass("glyphicon-triangle-right");
      $(".file-icon", folder).removeClass("glyphicon-folder-open").addClass("glyphicon-folder-close");
      $(folder).attr("data-expanded", "false");
      $(children).each(function () {
        $(this).hide();
      });
    }
    else {
      $(".folder-expand-icon", folder).removeClass("glyphicon-triangle-right").addClass("glyphicon-triangle-bottom");
      $(".file-icon", folder).removeClass("glyphicon-folder-close").addClass("glyphicon-folder-open");
      $(folder).attr("data-expanded", "true");
      $(children).each(function () {
        var parent = $(this).attr("data-parent");
        if ($("[data-id='" + parent + "']").attr("data-expanded") === "true") {
          $(this).show();
        }
      });
    }
    $("#table-files").stripTable();
  };


  /***************************************************************************/
  /* Ajax Functions (Form Processing)                                        */
  /***************************************************************************/

  /* Add file/folder */
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
        $("#id_name").focus().select();
        $("#table-files").stripTable();
      }
    });
  };

  /* Rename file/folder */
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
        $.cmdbox.fileRow = $(row);
        $(row).replaceWith(data.form);
        $("#id_name").focus().select();
        $("#table-files").stripTable();
      }
    });
  };

  /* Save file/folder */
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
          addFeaturedClass("info", data.file);
          delete $.cmdbox.fileRow;
        }
        else {
          $.cmdbox.alert("<span class='glyphicon glyphicon-warning-sign'></span> Warning", data.error);
          //$("#form-file").closest("tr").replaceWith(data.form);
          var row = $("#form-file").closest("tr");
          if ($.cmdbox.fileRow !== undefined) {
            $(row).replaceWith($.cmdbox.fileRow);
            delete $.cmdbox.fileRow;
          }
          else {
            $(row).remove();
          }
        }
      },
      complete: function () {
        $.cmdbox.stopLoading();
        $("#table-files").stripTable();
      }
    });
    return false;
  };

  var cancelFileFormEdit = function (event) {
    var key = event.which || event.keyCode;
    if (key === $.cmdbox.ESCAPE_KEY) {
      var row = $(this).closest("tr");
      if ($.cmdbox.fileRow !== undefined) {
        $(row).replaceWith($.cmdbox.fileRow);
        delete $.cmdbox.fileRow;
      }
      else {
        $(row).remove();
      }
      $("#table-files").stripTable();
    }
  };

  /* Delete file/folder */
  var loadDeleteFileDialog = function () {
    var btn = $(this);

    $.ajax({
      url: $(btn).attr("data-url"),
      type: 'get',
      cache: false,
      beforeSend: function () {
        $.cmdbox.loading();
      },
      success: function (data) {
        $("#modal-delete-file").html(data.html)
        $("#modal-delete-file").modal();
      },
      complete: function () {
        $.cmdbox.stopLoading();
      }
    });

  };

  var deleteFileBeforeSend = function () {
    $("#modal-delete-file").modal('hide');
  };

  var deleteFileSuccess = function (data) {
    var children = collectChildren(data.file);
    addFeaturedClass("danger", data.file, children, function () {
      $("#table-files tbody tr[data-id='" + data.file + "']").remove();
      $(children).each(function () {
        $(this).remove();
      });
      $("#table-files").stripTable();
    });
    $(".items-count").text(data.itemsCount);
  };

  /* Duplicate file/folder */
  var duplicateFile = function () {
    var url = $(this).attr("data-url");
    $.ajax({
      url: url,
      type: 'post',
      success: function (data) {
        $("#table-files tbody").html(data.html);
        $(".items-count").text(data.itemsCount);

        var children = collectChildren(data.file);
        addFeaturedClass("info", data.file, children);

        $("#table-files").stripTable();
      }
    });
  };


  /***************************************************************************/
  /* Binding                                                                 */
  /***************************************************************************/

  /* Add files/folders */
  $("main").on("click", ".js-add-file", loadAddFileForm);
  $("main").on("click", ".js-rename-file", loadRenameFileForm);
  $("main").on("keydown", "#id_name", cancelFileFormEdit);
  $("#table-files").on("submit", "#form-file", saveFile);
  $("main").on("blur", "#id_name", saveFile);

  /* Delete files/folders */
  $("main").on("click", ".js-delete-file", loadDeleteFileDialog);
  $.cmdbox.fn["#form-delete-file:deleteFileBeforeSend"] = deleteFileBeforeSend;
  $.cmdbox.fn["#form-delete-file:deleteFileSuccess"] = deleteFileSuccess;

  /* Duplicate files/folders */
  $("main").on("click", ".js-duplicate-file", duplicateFile);

  /* Expand/Contract folder */
  $("#table-files").on("click", "tbody tr[data-type='folder'] .file-name", toggleFolder);
  $("#table-files").on("click", "tbody tr[data-type='folder'] .folder-expand-icon", toggleFolder);


  /***************************************************************************/
  /* Main                                                                    */
  /***************************************************************************/

  var main = function () {
    $("#table-files").stripTable();
  };

  main();

});

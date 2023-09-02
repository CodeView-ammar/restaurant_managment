function update_elem_index(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+-)');
    var replacement = prefix + '-' + ndx + '-';
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,
        replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function add_form(btn, prefix) {
    var row_count = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());


    if (row_count < 1000) {
        var row = $(".form-row-purshess:last").clone(false).get(0);
          $(".errorlist", row).remove();
        $(".text-danger", row).remove();
        $(row).children().removeClass("error");
        $(row).children().removeClass("text-danger");
        $(row).find('td:first').text(row_count + 1);

        $(row).find('.formset-field').each(function() {
            update_elem_index(this, prefix, row_count)
            $(this).val(0);

        });
        $(row).find(".delete").click(function() {
            return delete_form(this, prefix);
        });
        $(row).insertAfter(".form-row-purshess:last").slideDown(300);

        $("#id_" + prefix + "-discount").val(0);
        $(`#id_${prefix}-${row_count}-item`).prop('required', true);

        $("#id_" + prefix + "-TOTAL_FORMS").val(row_count + 1);
    }

    return false;
}

function delete_form(btn, prefix) {
    var row_count = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());

    if (row_count > 1) {
        var goto_id = $(btn).find('input').val();
        if (goto_id) {
            $.ajax({
                url: "/" + window.location.pathname.split("/")[1] + "/formset-data-delete/" + goto_id + "/?next=" + window.location.pathname,
                error: function() {
                    console.log("error");
                },
                success: function(data) {
                    $(btn).parents('.form-row-purshess').remove();
                },
                type: 'GET'
            });
        } else {
            $(btn).parents('.form-row-purshess').remove();
        }

        var forms = $('.form-row-purshess');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        var i = 0;
        for (row_count = forms.length; i < row_count; i++) {
            $(forms.get(i)).find('.formset-field').each(function() {
                update_elem_index(this, prefix, i);
            });
        }
    } 
    return false;
}

$("body").on('click', '.remove', function() {
    delete_form($(this), String($('.add_row').attr('id')));
});

$("body").on('click', '.add_row', function() {

    return add_form($(this), String($(this).attr('id')));
});

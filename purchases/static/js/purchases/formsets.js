function update_elem_index(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+-)');
    var replacement = prefix + '-' + ndx + '-';
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,
        replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

// start for item unit formset
// var row_count = 0;
function add_form(btn, prefix) {
    var row_count = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());


    if (row_count < 1000) {
        var row = $(".form-row-purshess:last").clone(false).get(0);
        //       let tr = `<div id="div_id_${prefix}-${row_count}-item" class="form-group">


        //             <div class="">
        //                 <select name="${prefix}-${row_count}-item" class="formset-field clear-this modelselect2 form-control select2-hidden-accessible" style="width: 200px !important" onchange="getItemunit(this)"  id="id_${prefix}-${row_count}-item" data-autocomplete-light-language="en" data-autocomplete-light-url="/ItemAutocomplete1/" data-autocomplete-light-function="select2" data-select2-id="id_${prefix}-${row_count}-item" tabindex="-1" aria-hidden="true">
        // <option value="" selected="" data-select2-id="3">---------</option>
        // </select><span class="select2 select2-container select2-container--default select2-container--focus" dir="ltr" data-select2-id="4" style="width: 200px;"><span class="selection"><span class="select2-selection__rendered" id="select2-id_${prefix}-${row_count}-item-container" role="textbox" aria-readonly="true"><span class="select2-selection__placeholder"></span></span><span class="select2-selection__arrow" role="presentation"><b role="presentation"></b></span></span></span><span class="dropdown-wrapper" aria-hidden="true"></span></span>
        // </div></div>`;
        // $(row).find('.td_item').html(tr);
        $(".errorlist", row).remove();
        $(".text-danger", row).remove();
        $(row).children().removeClass("error");
        $(row).children().removeClass("text-danger");
        $(row).find('td:first').text(row_count + 1);

        //$(row).removeAttr('id').hide().insertAfter(".form-row-purshess:last").slideDown(300);
        $(row).find('.formset-field').each(function() {
            update_elem_index(this, prefix, row_count)
            $(this).val(0);

        });
        $(row).find(".delete").click(function() {
            return delete_form(this, prefix);
        });
        $(row).insertAfter(".form-row-purshess:last").slideDown(300);
        //$('#tblProducts').append(row);

        $("#id_" + prefix + "-discount").val(0);
        $(`#id_${prefix}-${row_count}-item`).prop('required', true);

        $("#id_" + prefix + "-TOTAL_FORMS").val(row_count + 1);
    }

    return false;
}

function delete_form(btn, prefix) {
    var row_count = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());

    if (row_count > 1) {
        // Delete the item/form
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
    } // End if
    return false;
}

$("body").on('click', '.remove', function() {
    delete_form($(this), String($('.add_row').attr('id')));
});

$("body").on('click', '.add_row', function() {

    return add_form($(this), String($(this).attr('id')));
});

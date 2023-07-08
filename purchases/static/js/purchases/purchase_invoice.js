$(document).ready(function() {
    $('.nav.navbar.navbar-static-top').toggleClass('margin-50');
    $('body.skin-blue.sidebar-mini').toggleClass('sidebar-collapse');

        $.ajax({
            url: "/get_code/",
            data: { },
            method: 'get',
            success: function(data) {

                if (data.status == 1) {
                    // console.log(data.data);

                    $('#id_code').val(data.data);
                    $('#id_code').attr('readonly', true);
                }
            },
            error: function(data) {}
        });


    $(document).on('click', '#PurchaseInvoicelocalDetails', function() {
        getAlltotal();
    });

    $(document).on('submit', '#myform_invoic', function(e) {
        
        let form_id = '#myform_invoic';
        $(".text-danger", form_id).remove();
        let i = is_valied();
        e.preventDefault();
        if (i) {
            $.ajax({
                url: $(this).attr('action'),
                data: $(this).serialize(),
                method: 'POST',
                success: function(data) {

                    $(".text-danger", form_id).remove();

                    if (data.status == 1) {
                        clearForm();
                        let invoice_rows = parseInt($('#id_' + 'PurchaseInvoicelocalDetails' + '-TOTAL_FORMS').val());
                        for (i = 0; i <= invoice_rows; i++) {
                            delete_form($('#PurchaseInvoicelocalDetails'), String($('.add_row').attr('id')));
                        }
                        alert(data.message);

                            // $('.datatable').DataTable().ajax.reload();
                    } else if (data.status == 2) {
                        $.each(data.error, function() {
                            let form = $(this)[0].form_id;
                            alert_message($(this)[0].message, 'alert alert-danger');
                        });
                    } else if (data.status == 0) {
                        console.log(data);
                        alert_message(data.message, data.class);


                        let invoice_rows = parseInt($('#id_' + 'PurchaseInvoicelocalDetails' + '-TOTAL_FORMS').val());

                        // if (data.message.message != '') {
                        //     alert_message(data.message.message, data.message.class);
                        // }


                        if (!data.error == "") {
                            alert(data.error);
                            let row_id = data.error.form_id;
                            let row_id2 = data.error['myform_invoic'];
                            let error = JSON.parse(data.error.error);
                            $.each(error, function(i, value) {
                                let div = '<span class="text-danger">';
                                $.each(value, function(j, message) {
                                    //console.log(message.message)
                                    div += `- ${message.message}<br>`;
                                });

                                $(`#id_${row_id}-0-${i}`).parent().append(div);
                            });
                        }
                        if (!data.error2 == "") {



                            let error2 = JSON.parse(data.error2);

                     
                            $.each(error2, function(i, value) {
                              
                                let div = '<span class="text-danger">';
                                $.each(value, function(j, message) {
                                    div += `- ${message.message}<br>`;
                                    alert_message(String(message.message), 'alert alert-warning', 'fa fa-times');
                                });
                                $(`#id_PurchaseInvoicelocalDetails-${data.row}-${i}`).parent().append(div);
                            });
                        }
                    } else if (data.status == 3) {
                        alert_message(data.message.message, data.message.class);
                        // alert_message(String(data.message + data.msg), 'alert alert-warning', 'fa fa-times');

                        //alert(data.message + data.msg)
                    }
                    $('#submit-button').button('reset');
                },
                error: function(data) {
                    // console.log(data)
                    //alert_message(String(data.message ), 'alert alert-warning', 'fa fa-times');


                    alert('fail');
                }
            });
        }
    });

    $(document).on('click', '.show_Operation>tr', function() {


        $('#myform_invoic').trigger("reset");
        let id_row = $(this).children('td:nth(0)').children('.row_span_id').data('id');
        $.ajax({
            url: $(this).children('td:nth(0)').children('.row_span_id').data('url'),
            data: { 'id': id_row, },
            method: 'get',
            success: function(data) {


                    $('.datatable').DataTable().ajax.reload();

                let form_data = JSON.parse(data.data1);
                // console.log(form_data[0].pk);
                let dataItem = data.dataitem
                let formset_data = JSON.parse(data.data2);
                let invoice_rows = parseInt($('#id_' + 'PurchaseInvoicelocalDetails' + '-TOTAL_FORMS').val());
                $(`input[name="id_invoice"]`).val(form_data[0].pk);
                if (data.status === 1) {
                    let supplierdata = data.datasupplier;
                    let supplier_optoin = `<option selected value="${supplierdata.id}">${supplierdata.name}</option>`;
                    $('#id_supplir').append(supplier_optoin);
                    if (form_data.length !== 0) {
                        $.each(form_data[0].fields, function(i, value) {
                            if (!$('#id_' + i).is(":text")) {
                                $(`textarea[name=${i}]`).text(value);

                            }
                            if (!$('#id_' + i).is(":checkbox")) {
                                $(`input[name="${i}"]`).val(value);
                            }
                            if ($('#id_' + i).is(":checkbox")) {
                                if (value === true) {
                                    $(`input[name="${i}"][type="checkbox"]`).val(value);
                                    $(`input[name="${i}"][type="checkbox"]`).attr('checked', 'checked');
                                }

                            }
                            $(`select[name="${i}"] option[value="${value}"]`).attr('selected', 'selected');
                            // $(`select[name="${i}"]`).val(value);

                        });
                        $('#delete_this').addClass('hidden');
                        // $('#delete_this').addAttr('style');
                        $('#add-row1').addClass('hidden');
                        $('#Previous_Operations').modal('hide');
                    }



                    if (formset_data.length !== 0) {
                        if (invoice_rows > 1) {

                            for (i = 0; i <= invoice_rows; i++) {
                                delete_form($('#PurchaseInvoicelocalDetails'), String($('.add_row').attr('id')));

                            }

                        }
                        //console.log(data.dataitem);
                        // let unitrowcounter = 0;
                        // $.each(formset_data, function() {
                        //     if (unitrowcounter != 0) {
                        //         add_form($('.add_row'), String($('.add_row').attr('id')));
                        //     }

                        //     $.each(formset_data[unitrowcounter].fields, function(i, value) {
                        //         // alert(value);

                        //         $(`input[name="PurchaseInvoicelocalDetails-${unitrowcounter}-${i}"]`).val(value);
                        //     });
                        //     let item_optoin = `<option selected value="${dataItem[unitrowcounter].id}">${dataItem[unitrowcounter].name_ar}</option>`;
                        //     $(`#id_PurchaseInvoicelocalDetails-${unitrowcounter}-item `).append(item_optoin);

                        //     // console.log("unit");
                        //     // let unit = $(`#id_PurchaseInvoicelocalDetails-${unitrowcounter}-unit`).val();
                        //     // console.log(unit);
                        //     // getItemunit(document.getElementById(`id_PurchaseInvoicelocalDetails-${unitrowcounter}-item`));
                        //     $(`#id_PurchaseInvoicelocalDetails-${unitrowcounter}-unit`).val(unit);
                            // getTotal(document.getElementById(`id_PurchaseInvoicelocalDetails-${unitrowcounter}-discount`));
                            unitrowcounter += 1;
                        // });
                    }
                    if (isNaN(document.getElementById('id_store'))) {
                        $(`#id_store`).val(formset_data[0].fields.store)
                    }
                    $(`#id_cost_center`).val(formset_data[0].fields.cost_center)
                    $('#Previous_Operations_close').trigger('click');
                    $('#id_payment_method').trigger('change');
                } else if (data.status == 3) {
                    alert_message(String(data.message + data.msg), 'alert alert-warning', 'fa fa-times');

                    // alert(data.message + data.msg)
                }
            },
            error: function(data) {}
        });
    });

    $(document).on('click', '#btn_delete', function(e) {
        var result = confirm("هل تريد حقا حذف الفاتورة");
        if (result) {
            let id_row = $("#id_invoice1").val();

            $.ajax({
                url: $(this).data('url'),
                data: {
                    'id': id_row,
                },
                method: 'delete',
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrf);
                },
                success: function(data) {


                    if (data.status == 1) {

                        $(form_id)[0].reset();
                        $(`textarea`).text('');
                        $('select').each(function() {
                            $(this).prop('selectedIndex', 0);
                            $(this).children("option").remove();
                        });
                        let invoice_rows = parseInt($('#id_' + 'PurchaseInvoicelocalDetails' + '-TOTAL_FORMS').val());
                        for (i = 0; i <= invoice_rows; i++) {
                            delete_form($('#PurchaseInvoicelocalDetails'), String($('.add_row').attr('id')));
                        }

                        alert_message(data.message.message, data.message.class);
                            $('.datatable').DataTable().ajax.reload();


                    } else if (data.status == 3) {

                        alert_message(String(data.message + data.msg), 'alert alert-warning', 'fa fa-times');

                        // alert(data.message + data.msg)
                    }
                        $('.datatable').DataTable().ajax.reload();
                    $('#delete_this').addClass('hidden');

                },
                error: function(data) {

                }
            });
        }
    });
}); //end ready Docuoment

function getItemunit(id) {
    if (RepeatInItem(id)) {
       
    }
}


 
function getTotal(element_id) {
    let index = element_id.name.split('-');
    let qty = 0;
    let price = 0;
    let discount = 0;
    let rate = 0;

    // if (!isNaN(parseInt(document.getElementById(`id_PurchaseInvoicelocalDetails-${index[1]}-discount_rate`).value))) {
    //     rate = parseInt(document.getElementById(`id_PurchaseInvoicelocalDetails-${index[1]}-discount_rate`).value);

    // }

    if (!isNaN(parseInt(document.getElementById(`id_PurchaseInvoicelocalDetails-${index[1]}-qty`).value))) {
        qty = parseInt(document.getElementById(`id_PurchaseInvoicelocalDetails-${index[1]}-qty`).value);
    }
    if (!isNaN(parseFloat(document.getElementById(`id_PurchaseInvoicelocalDetails-${index[1]}-price`).value))) {
        price = parseFloat(document.getElementById(`id_PurchaseInvoicelocalDetails-${index[1]}-price`).value);
    }
    if (!isNaN(parseFloat(document.getElementById(`id_PurchaseInvoicelocalDetails-${index[1]}-discount`).value))) {
        discount = parseFloat(document.getElementById(`id_PurchaseInvoicelocalDetails-${index[1]}-discount`).value);
    }
    let i = element_id.id;
    // if (i == `id_PurchaseInvoicelocalDetails-${index[1]}-discount_rate`) {
    //     discount = (qty * price * rate / 100);
    //     $(`#id_PurchaseInvoicelocalDetails-${index[1]}-discount`).val(discount)
    // }
    if (i == (`id_PurchaseInvoicelocalDetails-${index[1]}-discount`)) {
        rate = (discount * 100 / (qty * price));
        $(`#id_PurchaseInvoicelocalDetails-${index[1]}-discount_rate`).val(rate)
    }
    $(`#id_PurchaseInvoicelocalDetails-${index[1]}-total_price`).val((qty * price) - discount);
    getAlltotal();
    getAllDiscountItem();
}

function getAlltotal() {
    let total_debit = 0;
    $('input[id$="-total_price"]').each(function() {
        if (!isNaN(parseFloat($(this).val()))) {
            total_debit += parseFloat($(this).val());
        }
    });

    $("#id_total_amount").val(total_debit);
    getNettotal();

}

function getAllDiscountItem() {
    let total_debit = 0;
    $('input[id$="-discount"]').each(function() {
        if (!isNaN(parseFloat($(this).val()))) {
            total_debit += parseFloat($(this).val());
        }
    });
    $("#id_discount_item").val(total_debit);
}

function getNettotal() {
    let total = 0;
    let descount = 0;
    if (!isNaN(parseFloat($('#id_total_amount').val()))) {
        total = parseFloat($('#id_total_amount').val());
    }
    if (!isNaN(parseFloat($('#id_discount').val()))) {
        descount = parseFloat($('#id_discount').val());
    }
    $("#id_total_net_bill").val(total - descount);
}

function getPercentag(idelment) {
    let value1 = 0;
    let reat = 0;
    let total1 = 0;
    if (idelment.id === 'id_discount_rate') {
        if (!isNaN(parseFloat($('#id_discount_rate').val()))) {
            value1 = parseFloat($('#id_discount_rate').val());
        }
        if (!isNaN(parseFloat($('#id_total_amount').val()))) {
            total1 = parseFloat($('#id_total_amount').val());
        }
        $('#id_discount').val(value1 / 100 * total1)
    }
    if (idelment.id === 'id_discount') {
        if (!isNaN(parseFloat($('#id_discount').val()))) {
            value1 = parseFloat($('#id_discount').val());
        }
        if (!isNaN(parseFloat($('#id_total_amount').val()))) {
            total1 = parseFloat($('#id_total_amount').val());
        }
        $('#id_discount_rate').val(value1 * 100 / total1)
    }
    getNettotal();
}

function getPrice(element_id) {
    let index = element_id.name.split('-');
    let qty = 0;
    let total = 0;
    if (!isNaN(parseInt(document.getElementById(`id_PurchaseInvoicelocalDetails-${index[1]}-qty`).value))) {
        qty = parseInt(document.getElementById(`id_PurchaseInvoicelocalDetails-${index[1]}-qty`).value);
    }
    if (!isNaN(parseFloat(document.getElementById(`id_PurchaseInvoicelocalDetails-${index[1]}-total_price`).value))) {
        total = parseFloat(document.getElementById(`id_PurchaseInvoicelocalDetails-${index[1]}-total_price`).value);
    }
    $(`#id_PurchaseInvoicelocalDetails-${index[1]}-price`).val(total / qty);
    $(`#id_PurchaseInvoicelocalDetails-${index[1]}-discount`).val(0);
    getAlltotal();
    getAllDiscountItem();
}

function is_valied() {

    let div = '<span class="text-danger">';

    amount = 0;
    total1 = 0;
    check_amount = 0;
    if (!isNaN(parseFloat($('#id_total_net_bill').val()))) {
        total1 = parseFloat($('#id_total_net_bill').val());
    }
    if (!isNaN(parseFloat($('#id_check_amount').val()))) {
        check_amount = parseFloat($('#id_check_amount').val());
    }
    if (!isNaN(parseFloat($('#id_amount').val()))) {
        amount = parseFloat($('#id_amount').val());
    }
 
    if (amount != total1 && amount != 0) {
        div += `- ${"message_error_amount"}<br>`;
        alert_message("message_error_amount", 'alert alert-danger');
        $(`#id_amount`).parent().append(div);
        if (!check_amount < total1) {
            div = '<span class="text-danger">';
            div += `- ${"message_error_check_amount"}<br>`;
            $(`#id_check_amount`).parent().append(div);
            alert_message("message_error_check_amount", 'alert alert-danger');
        }
        return false;
    } else if ((check_amount > total1) && $("#id_payment_method").val() === '4') {
        
        div += `- ${"message_error_check_amount"}<br>`;
        $(`#id_check_amount`).parent().append(div);
        alert_message("message_error_check_amount", 'alert alert-danger');
        return false;
    } else return true;
}


function RepeatInItem(id) {
    let data = id.name;
    $('select[id$="-item"]').each(function() {
        if (this.name != data) {
            if (this.value == id.value) {
                alert("هذا الصنف موجود في الجدول");
                return false;
            }
        }
    });
    return true;
}

function clearForm() {
    let form_id = '#myform_invoic';
    $(form_id)[0].reset();
    $(`textarea`).text('');
    $('select[id$="-item"]').each(function() {
        $(this).children("option").remove();
    });
    $(`#id_supplir`).prop('selectedIndex', 0);;
    $('select').each(function() {
        $(this).prop('selectedIndex', 0);
        $("#cash").addClass("hidden");
        $("#check").addClass("hidden");
        $("#cash_check").addClass("hidden");
        $("#check_amount").addClass("hidden");
        //$(this).children("option").remove();
    });
}
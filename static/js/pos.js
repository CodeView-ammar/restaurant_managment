function calculator(id){
    let qty=parseFloat($("#input_quantity-"+id).val());
    let price=parseFloat($("#price-"+id).text());
    
    
    $("#total-"+id).text(qty*price);

}

$("#pos_table tbody").on("click",".quantity-up", function(e){
e.preventDefault();
    upcount(this);
    total_items()
})

function upcount(this_item){
    let id_item=$(this_item).data("id");
    let count_product=$("#input_quantity-"+id_item).val();
    let after_quantity=parseInt(count_product)+1
    $("#input_quantity-"+id_item).val(after_quantity);
    calculator(id_item);
    
}
$("#pos_table tbody").on("click",".quantity-down", function(e){
    e.preventDefault();
    downcount(this)
    total_items()
})
function downcount(this_item)
{
    let id_item=$(this_item).data("id");
    let count_product=$("#input_quantity-"+id_item).val();
    if(parseInt(count_product)==1)
        return false
    let after_quantity=parseInt(count_product)-1
    $("#input_quantity-"+id_item).val(after_quantity);
    calculator(id_item);
    
}


$(".product_list").on("click",function(e) {
    e.preventDefault();
    let id_item=$(this).data("id");
    let name_item=$("#item-"+id_item).text();
    let price_item=$("#price-"+id_item).text();
    const existingItem = $("#pos_table tbody").find("[data-row_index='" + id_item + "']");
    if (existingItem.length) {
        upcount(this);
        total_items();
        return false;
    }
    
    $("#pos_table tbody ").append(
`   <tr class="product_row" data-row_index="${id_item}">
    <td>

            <div data-toggle="tooltip" data-placement="bottom" title="Edit product Unit Price and Tax">
            
                ${name_item}
            </div>

            <!-- Description modal end -->

        </td>

        <td>


            <div class="input-group input-number">
                <span class="input-group-btn">
                    <button type="button" class="btn btn-default btn-flat quantity-up" data-id=${id_item}>
                        <i class="fa fa-plus text-success"></i></button>
                    </span>
                    <input type="number" min="1" class="form-control pos_quantity input_number mousetrap input_quantity-${id_item} valid" id="input_quantity-${id_item}" value="1" name="products_quantity" >
                    <span class="input-group-btn">
                        <button type="button" class="btn btn-default btn-flat quantity-down" data-id=${id_item}><i class="fa fa-minus text-danger"></i></button>
                    </span>
            </div>

        
        </td>
        <td>

            <div data-toggle="tooltip" data-placement="bottom" id="price-${id_item}" >
            
                ${price_item}
            </div>

            <!-- Description modal end -->

        </td>

        <td class="text-center v-center">

            <span class="display_currency pos_line_total_text " id="total-${id_item}" data-currency_symbol="true">
            
            </span>
        </td>
        <td class="text-center">
            <a class="delete_row" id="" data-id="3" title=""><i class="fa fa-trash"></i></a>
        </td>
        </tr>`
)
calculator(id_item);
total_items()
})

function total_items(){
    let total_items_=0;
    $(".pos_line_total_text").each(function(){
        
        total_items_+=parseFloat($(this).text())
    });
    $(".price_total").text(total_items_);
}

$("#pos_table tbody").on("click", ".delete_row", function(e) {
    e.preventDefault();
    let id_item = $(this).data("id");
    $(this).parent().parent().html(""); 
  });
//add-review


const monthNames = [
    "Jan", // January
    "Feb", // February
    "Mar", // March
    "Apr", // April
    "May", // May
    "Jun", // June
    "Jul", // July
    "Aug", // August
    "Sep", // September
    "Oct", // October
    "Nov", // November
    "Dec"  // December
];





$("#commentForm").submit(function (e) {
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDate() +"  "+ monthNames[dt.getUTCMonth()] + " ," + dt.getFullYear()

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function (response) {
            console.log("Comment Saved to DB..");

            if (response.bool === true) {
                $("#review-rsp").html("Review added successfully.");
                $(".hide-comment-form").hide();
                $(".add-review").hide();

                let _html = '<tr>';
                _html += '<td>';
                _html += '<img src="../../static/img/logo/img.png" alt="Image" class="img-fluid mr-3 mt-1 rounded" style="width: 50px;">';
                _html += '<a href="" class="font-heading text-brand">' + response.context.user + '</a>';
                _html += '</td>';

                _html += '<td>';
                _html += '<span class="text-xs text-muted"><small>' + time + '</small></span>';
                _html += '</td>';



                _html += '<td>';
                for (let i = 1; i <= 5; i++) {
                    if (i <= response.context.rating) {
                        _html += '<i class="fas fa-star text-warning"></i>';
                    } else {
                        _html += '<i class="far fa-star text-warning"></i>';
                    }
                }
                _html += '</td>';

                _html += '<td>' + response.context.review + '</td>';
                _html += '</tr>';

                $(".comment-list tbody").prepend(_html);

                // Append this line to log a message when the rating is added successfully
                console.log("Rating added successfully: " + response.context.rating);
            }
        },
        error: function (error) {
            console.error("Error in AJAX request:", error);
        }
    });
});



// filter by category, vendor


$(document).ready(function () {
    $(".filter-checkbox").on("click", function () {
        let filter_object = {};

        $(".filter-checkbox").each(function () {
            let filter_value = $(this).val();
            let filter_key = $(this).attr("data-filter-title");

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter-title="' + filter_key + '"]:checked')).map(function (element) {
                return element.value;
            });
        });

        console.log(filter_object);
        $.ajax({
            url:'/filter-products',
            data: filter_object,
            dataType: 'json',
            beforeSend: function () {
                console.log("Trying to filter product...");
            },
            success: function (response) {
                console.log(response);
                console.log("Data filtered successfully...");

                $('#filtered-products').html(response.data)
            }
        })

    })

    /// add-to-cart
    $(".add-to-cart-btn").on("click", function () {
        let this_val = $(this)
        let index = this_val.attr("data-index")

        let quantity = $(".product-quantity-" + index).val()
        let product_title = $(".product-title-" + index).val()

        let product_id = $(".product-id-" + index).val()
        let product_price = $(".current-product-price-" + index).text()

        let product_pid = $(".product-pid-" + index).val()
        let product_image = $(".product-image-" + index).val()


        console.log("Quantity:", quantity);
        console.log("Title:", product_title);
        console.log("Price:", product_price);
        console.log("Id:", product_id);
        console.log("PID:", product_pid);
        console.log("Image:", product_image);


        console.log("Current Element:", this_val);

        $.ajax({
            url:'/add-to-cart',
            data:{
                'id':product_id,
                'pid':product_pid,
                'image':product_image,
                'qtty':quantity,
                'title':product_title,
                'price':product_price,


            },
            dataType:'json',
            beforeSend:function () {
                console.log("Adding Product to cart...")


            },
            success:function (response) {
                this_val.html("✅")
                console.log("Added item to cart!!")
                $(".cart-items-count").text(response.totalcartitems)

            }
        })


    })


//deleting from cart

    $(".delete-product").on("click", function () {

        let product_id = $(this).attr("data-product")
        let this_val = $(this)

        console.log("PRoduct ID:", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data:{
                "id": product_id,

            },
            dataType: "json",
            beforeSend: function () {
                this_val.hide()
            },
             success: function (response) {
                 this_val.show()
                  $(".cart-items-count").text(response.totalcartitems)
                 $("#cart-list").html(response.data)
             }
        })

    })



    ///updating -cart

    $(".update-product").on("click", function () {

        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_quantity = $(".product-qtty-" + product_id).val()

        console.log("PRoduct ID:", product_id);
        console.log("PRoduct QTTY:", product_quantity);

        $.ajax({
            url: "/update-cart",
            data:{
                "id": product_id,
                "qtty": product_quantity,

            },
            dataType: "json",
            beforeSend: function () {
                this_val.hide()
            },
             success: function (response) {
                 this_val.show()
                  $(".cart-items-count").text(response.totalcartitems)
                 $("#cart-list").html(response.data)
             }
        })

    })

})






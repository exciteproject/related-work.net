$(document).ready(function () {
    $("#form-search").submit(function( event ) {
    var query = $("#q").val();
    $("#ul_results").empty();
    $.get("/search_arxiv/" + query, function (data, status) {
        data.forEach(function (item, index) {
            $("#ul_results").append(
                $('<li>').append(
                    $("<a>").attr('href', '/preview/#'+item.meta_id).text(item.author + ',' + item.title)
                )
            );
        });

    });
    event.preventDefault();
});
});

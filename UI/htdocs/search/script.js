$(document).ready(function () {
    $("#form-search").submit(function( event ) {
    var query = $("#q").val();
    $("#ul_results").empty();
    $.get("/search_arxiv/" + query, function (data, status) {
        if(data.length == 0){
            $("#ul_results").append(
                $('<li>').text("No results found"));
        }
        data.forEach(function (item, index) {
            $("#ul_results").append(
                $('<li>').append(
                    $("<a>").attr('href', '/preview/#'+item.meta_id).text(item.author + ', ').append(
                        $("<em>").text(item.title)
                    )
                )
            );
        });

    });
    event.preventDefault();
});
});

function loadResults(query){
    $("#ul_results").empty();
    $("#title_q").text(query);
    window.history.pushState('Page', 'Title', '/search/#' + query);
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
                    ).append("<span> (Cited: " + item.citations + ")</span>")
                )
            );
        });

    });
}
$(document).ready(function () {
    loadResults(window.location.hash.substring(1) || "colorful");

    $("#form-search").submit(function( event ) {
        var query = $("#q").val();
        loadResults(query);
        event.preventDefault();
    });
});

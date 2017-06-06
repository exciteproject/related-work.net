window.onhashchange = function () {
    loadResults(window.location.hash.substring(1) || "colorful");
};
function loadResults(query) {
    $("#loader").show();
    $("#ul_results").empty();
    $("#title_q").text(query);
    window.history.pushState('Page', 'Title', '/#' + query);
    $.get("/search_arxiv/" + query, function (data, status) {
        $("#loader").hide();
        if (data.length == 0) {
            $("#ul_results").append(
                $('<li>').text("No results found"));
        }
        data.forEach(function (item, index) {
            $("#ul_results").append(
                $('<li>').append(
                    $("<a>").attr('href', '/preview/#' + item.meta_id).text(item.author + ', ').append(
                        $("<em>").text(item.title)
                    ).append("<span> (Cited: " + item.citations + ")</span>")
                )
            );
        });

    });
}
$(document).ready(function () {
    loadResults(window.location.hash.substring(1) || "colorful");

    $("#form-search").submit(function (event) {
        $("#loader").show();
        var query = $("#q").val();
        loadResults(query);
        event.preventDefault();
    });
});

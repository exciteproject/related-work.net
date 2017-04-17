window.onhashchange = function() {
    loadid(window.location.hash.substring(1) || "1305.2467");
};
function loadid(id) {
    // $("#preview").attr("src", "https://arxiv.org/pdf/" + id + ".pdf");
    $("#preview").get(0).contentWindow.location.replace("https://arxiv.org/pdf/" + id + ".pdf");
    $.get("/meta/" + id, function (data, status) {
        var rec = data[0];
        if (rec === null) {
            $(".title").text("Metadata not available");
            $("#meta_id").text(id);
            $(".author").text("");
            // $("#p_abstract").text("");
            return
        }
        $("#meta_id").text(rec['meta_id']);
        $(".title").text(rec['title']);
        $(".author").text(rec['author']);
        // $("#p_abstract").text(rec['abstract']);
    });
    $.get("/citations/" + id, function (data, status) {
        var reflist = $("#ul_citations");
        reflist.empty();
        for (var i = 0; i < data.length; i++) {
            reflist.append(
                $('<li>').append(
                    $('<a>').text('[' + data[i].meta_id_source + '] :: ' + data[i].author + ", ").append(
                        $('<em>').text(data[i].title))).click(data[i].meta_id_source, loadev).append(
                        $('<br>')
                    ).append('Reference: "' + data[i].ref_text + '"')
                );
        }
    });
    $.get("/references/" + id, function (data, status) {
        var reflist = $("#ul_references");
        reflist.empty();
        data.sort(function (a, b) {
            a = a.meta_id_target;
            b = b.meta_id_target;
            return (a === null) - (b === null) || +(a > b) || -(a < b);
        });
        for (var i = 0; i < data.length; i++) {
            if (data[i].meta_id_target === null) {
                reflist.append(
                    $('<li>').text(data[i].ref_text)
                );
            } else {
                reflist.append(
                $('<li>').append(
                    $('<a>').text('[' + data[i].meta_id_target + '] :: ' + data[i].author + ", ").append(
                        $('<em>').text(data[i].title))).click(data[i].meta_id_target, loadev).append(
                        $('<br>')
                    ).append('Reference: "' + data[i].ref_text + '"')
                );
            }
        }
    });
}
function loadev(ev) {
    var meta_id = ev.data;
    window.history.pushState('Page', 'Title', window.location.pathname + '#' + meta_id);
    loadid(meta_id);
}
$(document).ready(function () {
    loadid(window.location.hash.substring(1) || "1305.2467");
});

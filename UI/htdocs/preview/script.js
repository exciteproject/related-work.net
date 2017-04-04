function loadid(id) {
    $("#preview").attr("src", "https://arxiv.org/pdf/" + id + ".pdf");
    $.get("/meta/" + id, function (data, status) {
        var rec = data[0];
        if (rec === null) {
            $("#title").text("Metadata not available");
            $("#meta_id").text(id);
            $("#author").text("");
            $("#p_abstract").text("");
            return
        }
        $("#meta_id").text(rec['meta_id']);
        $("#title").text(rec['title']);
        $("#author").text(rec['author']);
        $("#p_abstract").text(rec['abstract']);
    });
    $.get("/citations/" + id, function (data, status) {
        var reflist = $("#ul_citations");
        reflist.empty();
        for (var i = 0; i < data.length; i++) {
            load_citation_meta(data[i].meta_id_source, data[i].ref_text);
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
            var li = document.createElement("li");
            if (data[i].meta_id_target === null) {
                li.textContent = data[i].ref_text;
            } else {
                var a = document.createElement("a");
                a.textContent = '[' + data[i].meta_id_target + '] :: ' + data[i].ref_text;
                $(a).click(data[i].meta_id_target, loadev);
                li.appendChild(a);
            }
            reflist.append(li);
        }
    });
}
function loadev(ev) {
    var meta_id = ev.data;
    window.history.pushState('Page', 'Title', '/#' + meta_id);
    loadid(meta_id);
}
function load_citation_meta(meta_id_source, ref_text) {
    var reflist = $("#ul_citations");
    $.get("/meta/" + meta_id_source, function (metadata) {
        var rec = metadata[0];
        reflist.append(
            $('<li>').append(
                $('<a>').text('[' + meta_id_source + '] :: ' + rec['author'] + ", ").append(
                    $('<em>').text(rec['title']))).click(meta_id_source, loadev).append(
                    $('<br>')
                ).append('Reference: "' + ref_text + '"')
            );
    });
}
$(document).ready(function () {
    loadid(window.location.hash.substring(1) || "1305.2467");
});

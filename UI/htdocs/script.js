function loadid(id) {
    $("#preview").attr("src", "https://arxiv.org/pdf/" + id + ".pdf");
    $.get("/meta/" + id, function(data, status){
        var rec = data[0];
        if(!'meta_id' in rec){return}
        $("#meta_id").text(rec['meta_id']);
        $("#title").text(rec['title']);
        $("#author").text(rec['author']);
        $("#p_abstract").text(rec['abstract']);
    });
    $.get("/references/" + id, function(data, status){
        var reflist = $("#ul_references");
        reflist.empty();
        for(var i=0; i<data.length; i++) {
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.textContent = '[' + data[i].meta_id_target + '] :: ' + data[i].ref_text;
            $(a).click(data[i].meta_id_target, loadev);
            li.appendChild(a);
            reflist.append(li);
        }
    });
    $.get("/citations/" + id, function(data, status){
        var reflist = $("#ul_citations");
        reflist.empty();
        for(var i=0; i<data.length; i++) {
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.textContent = '[' + data[i].meta_id_source + '] :: ' + data[i].ref_text;
            $(a).click(data[i].meta_id_source, loadev);
            li.appendChild(a);
            reflist.append(li);
        }
    });
}
function loadev(ev) {
    var meta_id = ev.data;
    window.history.pushState('Page', 'Title', '/#' + meta_id);
    loadid(meta_id);
}
$(document).ready(function(){
    loadid(window.location.hash.substring(1) || "1305.2467");
});

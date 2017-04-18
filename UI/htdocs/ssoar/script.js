window.onhashchange = function() {
    loadid(window.location.hash.substring(1) || "20811-32266");
};
function loadid(id) {
    // $("#preview").attr("src", "http://excite-compute.west.uni-koblenz.de/ssoar/" + id + ".pdf");
    $("#preview").get(0).contentWindow.location.replace("http://excite-compute.west.uni-koblenz.de/ssoar/" + id + ".pdf");
    // $.get("/meta/" + id, function(data, status){
    //     var rec = data[0];
    //     $("#meta_id").text(rec['meta_id']);
    //     $(".title").text(rec['title']);
    //     $(".author").text(rec['author']);
    //     $("#p_abstract").text(rec['abstract']);
    // });
    $.get("/ssoar-json/" + id, function(data, status){
        var reflist = $("#ul_references");
        reflist.empty();
        for(var i=0; i<data.length; i++) {
            var li = document.createElement("li");
            li.textContent = data[i].ref_text;
            reflist.append(li);
        }
    });
}
function loadev(ev) {
    var meta_id = ev.data;
    window.history.pushState('Page', 'Title', window.location.pathname + '#' + meta_id);
    loadid(meta_id);
}
$(document).ready(function(){
    loadid(window.location.hash.substring(1) || "20811-32266");
});

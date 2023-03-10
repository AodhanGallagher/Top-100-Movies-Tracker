// Function used to update the 'watched movie' button to indicate that a movie has seen
function changeState(movie_id) {
    $("#"+movie_id).removeClass("btn-light").addClass("btn-success");
    $("#"+movie_id).val("Seen");
}
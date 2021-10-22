window.onload = function() {
    var submit_btn = document.getElementById("submit_btn");

    var loading_btn = document.getElementById("loading_btn");

    document.querySelector('form').addEventListener('submit', functSubmit);

    function functSubmit(event) {
    submit_btn.classList.add("d-none");
    loading_btn.classList.remove("d-none");

    }

}



var iframe = document.querySelector("#form iframe");

function reloadPrewiew() {
    var id = document.querySelector("#uid").value;
    var cid = document.querySelector("#id").value;
    var flag = document.querySelector("#flag").value;
    var names = document.querySelector("#name").value;
    var group = document.querySelector("#group").value;
    var goverment_type = document.querySelector("#goverment_type_check").value;
    var goverment_form = document.querySelector("#goverment_form_check").value;
    var ideology = document.querySelector("#ideology_check").value;
    var political_type = document.querySelector("#political_type_check").value;
    var date = document.querySelector("#date").value;
    var desc = document.querySelector("#desc").value;

    iframe.setAttribute("src", `/countries/prewiew?id=${id}&cid=${cid}&flag=${flag}&name=${names}&group=${group}&goverment_type=${goverment_type}&goverment_form=${goverment_form}&ideology=${ideology}&political_type=${political_type}&date=${date}&desc=${desc}&check=query`);
}
// TODO: Перенос данных о заправке в веб форму

is_edit = false

function editRow(row_id) {
    if (is_edit == false) {
        var work_row = document.querySelector(".work_table_row.num_" + row_id)
        var form_cols = work_row.querySelectorAll(".form_col")
        var table_cols = work_row.querySelectorAll(".table_col")
        for (e in table_cols) {
            console.log(e.innerHTML)
        }
        form_cols[0].querySelector(".id").defaultValue = row_id
        form_cols[1].querySelector(".date").defaultValue = table_cols[1].innerHTML
        form_cols[2].querySelector(".odometer").defaultValue = table_cols[2].innerHTML
        var option = document.createElement("option")
        option.value = table_cols[0].innerHTML
        option.text = table_cols[3].innerHTML
        form_cols[3].querySelector(".station").add(option)
        form_cols[4].querySelector(".gallons").defaultValue = table_cols[4].innerHTML
        for (var i = 1; i < form_cols.length; i++) {
            form_cols[i].style.display = "table-cell"
            table_cols[i].style.display = "none"
        }
        work_row.style.backgroundColor = "#808080"
        is_edit = true
    }
    else {
        alert("Сохраните редактируемую строку!")
    }
}


function saveRow() {
    is_edit = false
}
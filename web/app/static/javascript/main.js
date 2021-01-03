// TODO: Перенос данных о заправке в веб форму

is_edit = false

function editRow(row_id, station_id) {
    if (is_edit == false) {
        var work_row = document.querySelector(".work_table_row.num_" + row_id)
        var form_cols = work_row.querySelectorAll(".form_col")
        var table_cols = work_row.querySelectorAll(".table_col")
        var fuel_data = document.querySelector(".navig_form.names").querySelectorAll("option")
        form_cols[0].querySelector(".id").defaultValue = row_id
        form_cols[1].querySelector(".date").defaultValue = table_cols[0].innerHTML
        form_cols[2].querySelector(".odometer").defaultValue = table_cols[1].innerHTML
        var option = document.createElement("option")
        option.value = station_id
        option.text = table_cols[2].innerHTML
        form_cols[3].querySelector(".station").add(option)
        for (var i = 0; i < fuel_data.length; i++) {
            console.log(fuel_data[i])
            var opt = document.createElement("option")
            if ( fuel_data[i].value == station_id) {
                continue
            }
            else {
                opt.value = fuel_data[i].value
                opt.text = fuel_data[i].text
            }
            form_cols[3].querySelector(".station").add(opt)
        }
        form_cols[4].querySelector(".gallons").defaultValue = table_cols[3].innerHTML
        for (var i = 1; i < form_cols.length; i++) {
            form_cols[i].style.display = "table-cell"
            table_cols[i - 1].style.display = "none"
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
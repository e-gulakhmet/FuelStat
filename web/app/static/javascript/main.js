// TODO: Перенос данных о заправке в веб форму

is_edit = false

function editRow(row_id) {
    if (is_edit == false) {
        let work_row = document.querySelector(".work_table_row.num_" + row_id)
        let form_cols = work_row.querySelectorAll(".form_col")
        let table_cols = work_row.querySelectorAll(".table_col")
        let form_names = [".date", ".odometer", ".station", ".gallons"]

        form_cols[0].querySelector(".id").defaultValue = row_id
        for (let i = 1; i < form_cols.length; i++) {
            if (i == 3) {
                let option = document.createElement("options")
                option.innerHTML = "Fuck"
                form_cols[i].querySelector(form_names[i - 1]).appendChild(option)
            }
            else if (i != 5){
                // Получаю еще один объкет из form_cols, так как в form_cols содежраться input, а уже в них
                // нужно заменить значения. А в tale_cols содержаться значения, которые нужно присвоить input,
                // который находиться в form_cols
                form_cols[i].querySelector(form_names[i - 1]).defaultValue = table_cols[i - 1].innerHTML
            }
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
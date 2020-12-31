
// TODO: Перенос данных о заправке в веб форму

function editRow(row_id) {
    let work_row = document.querySelector(".work_table_row.num_" + row_id)
    let form_cols = work_row.querySelectorAll(".form_col")
    let table_cols = work_row.querySelectorAll(".table_col")
    let form_names = [".date", ".odometer", ".station", ".gallons"]

    for (let i = 0; i < form_cols.length; i++) {
        if (i == 2) {
            let option = document.createElement("options")
            option.innerHTML = "Fuck"
            form_cols[i].querySelector(form_names[i]).appendChild(option)
        }
        else if (i != 4){
            // Получаю еще один объкет из form_cols, так как в form_cols содежраться input, а уже в них
            // нужно заменить значения. А в tale_cols содержаться значения, которые нужно присвоить input,
            // который находиться в form_cols
            form_cols[i].querySelector(form_names[i]).defaultValue = table_cols[i].innerHTML
        }
        form_cols[i].style.display = "table-cell"
        table_cols[i].style.display = "none"
    }
    work_row.style.backgroundColor = "#808080"
}
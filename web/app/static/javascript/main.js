function editRow(row_id) {
    let date = document.querySelector(".row_form.date")
    let odometer = document.querySelector(".row_form.odometer")
    let station = document.querySelector(".row_form.fuel_station")
    let gallon = document.querySelector(".row_form.gallon_count")
    date.style.display = "block"
    odometer.style.display = "block"
    station.style.display = "block"
    gallon.style.display = "block" 
    console.log(row_id)   
}
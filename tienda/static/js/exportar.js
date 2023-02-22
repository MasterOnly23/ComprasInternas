// Función para convertir las comas en puntos en un valor dado
function convertCommaToDot(value) {
    // Convertir el valor a una cadena y reemplazar las comas con puntos
    return value.toString().replace(",", ".");
}

// Función para exportar una tabla a un archivo Excel
function exportExcel(tablaID) {
    // Obtener la tabla del documento HTML mediante su ID
    var table = document.getElementById(tablaID);
    // Obtener todas las filas de la tabla
    var rows = table.getElementsByTagName("tr");
    // Recorrer todas las filas
    for (var i = 0; i < rows.length; i++) {
        // Obtener todas las celdas de la fila actual
        var cells = rows[i].getElementsByTagName("td");
        // Recorrer todas las celdas
        for (var j = 0; j < cells.length; j++) {
            // Convertir las comas en puntos en el contenido de la celda actual
            cells[j].innerHTML = convertCommaToDot(cells[j].innerHTML);
        }
    }
    // Crear un libro de trabajo de Excel a partir de la tabla
    var wb = XLSX.utils.table_to_book(table);
    // Obtener la fecha actual
    var fecha = new Date();
    // Crear un nombre de archivo utilizando la fecha actual
    var nombreArchivo = "Ordenes_"+fecha.getDate()+"-"+(fecha.getMonth()+1)+"-"+fecha.getFullYear()+".xlsx"
    // Escribir el libro de trabajo en un archivo con el nombre especificado
    XLSX.writeFile(wb, nombreArchivo);
}

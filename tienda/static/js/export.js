// Función para convertir las comas en puntos en un valor dado
function convertCommaToDot(value) {
    // Convertir el valor a una cadena y reemplazar las comas con puntos
    return value.toString().replace(",", ".");
}

// Función para eliminar una columna de una tabla
function removeTableColumn(table, columnIndex) {
    // Obtener todas las filas de la tabla
    var rows = table.getElementsByTagName("tr");
    // Recorrer todas las filas
    for (var i = 0; i < rows.length; i++) {
        // Eliminar la celda en el índice especificado
        rows[i].deleteCell(columnIndex);
    }
}

// Función para exportar una tabla a un archivo Excel
function exportExcel(tablaID, columnsToRemove, fileName) {
    // Obtener la tabla del documento HTML mediante su ID
    var table = document.getElementById(tablaID);
    // Crear una copia de la tabla
    var tableCopy = table.cloneNode(true);
    // Ordenar el array de columnas a eliminar de menor a mayor
    columnsToRemove.sort((a,b) => a-b);
    // Recorrer el array de columnas a eliminar
    for (var i = 0; i < columnsToRemove.length; i++) {
        // Eliminar la columna especificada de la copia de la tabla
        removeTableColumn(tableCopy, columnsToRemove[i] - i);
    }
    // Recorrer todas las filas de la tabla copiada
    var rows = tableCopy.getElementsByTagName("tr");
    for (var i = 0; i < rows.length; i++) {
        // Obtener todas las celdas de la fila actual
        var cells = rows[i].getElementsByTagName("td");
        // Recorrer todas las celdas
        for (var j = 0; j < cells.length; j++) {
            // Convertir las comas en puntos en el contenido de la celda actual
            cells[j].innerHTML = convertCommaToDot(cells[j].innerHTML);
        }
    }
    // Crear un libro de trabajo de Excel a partir de la tabla copiada
    var wb = XLSX.utils.table_to_book(tableCopy);
    // Obtener la fecha actual
    var fecha = new Date();
    // Crear un nombre de archivo utilizando la fecha
    // var nombreArchivo = "Productos_"+fecha.getDate()+"-"+(fecha.getMonth()+1)+"-"+fecha.getFullYear()+".xlsx"
    // Escribir el libro de trabajo en un archivo con el nombre especificado
    XLSX.writeFile(wb, fileName);
}

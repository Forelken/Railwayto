document.addEventListener('DOMContentLoaded', function() {
    const containers = document.querySelectorAll('.table-container');

    containers.forEach(container => {
        const headers = container.querySelectorAll('th');
        const createButton = container.querySelector('.create');
        const tableName = container.dataset.table.toLowerCase(); // Приводим имя таблицы к нижнему регистру
        const table = container.querySelector('table tbody');

        // Обработчик двойного нажатия на ячейку заголовка для сортировки
        headers.forEach(header => {
            if (header.textContent.trim() !== 'Действия') {
                header.addEventListener('dblclick', function() {
                    // Удаляем классы сортировки у всех заголовков
                    headers.forEach(h => {
                        h.classList.remove('sort-asc');
                        h.classList.remove('sort-desc');
                    });

                    const field = header.dataset.field;
                    const isAscending = header.classList.toggle('ascending');

                    if (isAscending) {
                        header.classList.add('sort-asc');
                    } else {
                        header.classList.add('sort-desc');
                    }

                    const data = {
                        table: tableName,
                        field: field,
                        order: isAscending ? 'asc' : 'desc'
                    };

                    console.log('Sending data:', data); // Логирование данных

                    fetch(`/sort_table`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(data)
                    })
                    .then(response => response.text())
                    .then(html => {
                        table.innerHTML = html;
                        addTableEventListeners(table); // Добавляем обработчики событий для редактирования
                        console.log('Event listeners added to new table rows'); // Логирование
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                });
            }

            // Добавляем обработчики событий для редактирования к начальной таблице
            addTableEventListeners(table);
        });

        

        // Обработчик для кнопки "Create"
        createButton.addEventListener('click', function() {
            const newRow = document.createElement('tr');
            const headers = container.querySelectorAll(`th[data-field]`);
            let rowHtml = '';
            headers.forEach(header => {
                const fieldName = header.dataset.field;
                if (fieldName !== 'Actions' && !fieldName.endsWith('_id')) {
                    rowHtml += `<td contenteditable="true" data-field="${fieldName}"></td>`;
                }
            });
            rowHtml += `
                <td>
                    <button class="table-button confirm" onclick="confirmRow(this)">Подтвердить</button>
                    <button class="table-button cancel" onclick="cancelRow(this)">Отмена</button>
                </td>
            `;
            newRow.innerHTML = rowHtml;
            table.appendChild(newRow);
        });
    });

    var directionId = document.getElementById('direction_id').value;
        fetch('/get_seats_for_' + directionId)
            .then(response => response.json())
            .then(data => {
                var seatSelect = document.getElementById('seat_id');
                seatSelect.innerHTML = '';
                data.forEach(seat => {
                    var option = document.createElement('option');
                    option.value = seat.seat_id;
                    option.textContent = `${seat.class_field} - ${seat.seat_place} - ${seat.carriage} - ${seat.train_id}`;
                    seatSelect.appendChild(option);
                });
            });
});

function addTableEventListeners(tbody) {
    const cells = tbody.querySelectorAll('td');
    cells.forEach(cell => {
        cell.addEventListener('dblclick', function() {
            console.log('Double click event added to cell:', cell); // Логирование
            const originalValue = cell.textContent;
            cell.contentEditable = true;
            cell.focus();

            // Сохраняем текущий порядок строк таблицы
            const tableRows = Array.from(cell.parentElement.parentElement.rows);

            cell.addEventListener('blur', function() {
                const newValue = cell.textContent;
                if (originalValue !== newValue) {
                    updateCell(cell, newValue, tableRows);
                }
                cell.contentEditable = false;
            }, { once: true });
        });
    });
}

function updateCell(cell, newValue, tableRows) {
    const row = cell.parentElement;
    const tableName = row.closest('.table-container').dataset.table;
    const pk = row.dataset.pk;
    const field = cell.dataset.field;

    fetch(`/update_cell`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            table: tableName,
            pk: pk,
            field: field,
            value: newValue
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            cell.textContent = newValue;
            // Восстанавливаем порядок строк таблицы
            const tableBody = cell.parentElement.parentElement;
            tableBody.innerHTML = '';
            tableRows.forEach(row => tableBody.appendChild(row));
        } else {
            alert('Error updating cell');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function confirmRow(button) {
    const row = button.closest('tr');
    const tableName = row.closest('.table-container').dataset.table.toLowerCase(); // Приводим имя таблицы к нижнему регистру
    const data = {};
    const cells = row.querySelectorAll('td[data-field]');
    cells.forEach(cell => {
        data[cell.dataset.field] = cell.textContent.trim();
    });

    console.log('Sending data:', { table: tableName, fields: data }); // Логирование данных

    fetch('/create_item', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            table: tableName,
            fields: data
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            row.setAttribute('data-pk', data.id);
            let rowHtml = '';
            for (const field in data) {
                if (field !== 'id') {
                    rowHtml += `<td data-field="${field}">${data[field]}</td>`;
                }
            }
            rowHtml += `
                <td>
                    <a class="table-button view" href="/get_${tableName}/${data.id}">Подробнее</a>
                    <button class="table-button delete" onclick="deleteItem('${tableName}s', '${data.id}')">Удалить</button>
                </td>
            `;
            row.innerHTML = rowHtml;
        } else {
            alert('Error creating item: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function cancelRow(button) {
    const row = button.closest('tr');
    row.remove();
}

function toggleAdmin(userId) {
    console.log(userId);
    fetch('users/toggle_admin/' + userId, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();  // Обновить страницу после успешного изменения
        } else {
            alert('Error toggling admin status');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function deleteItem(itemType, itemId) {
    if (confirm('Are you sure you want to delete this ' + itemType + '?')) {
        console.log('Deleting item:', itemType, itemId); // Логирование данных
        fetch('/' + itemType + '/' + itemId + '/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();  // Обновить страницу после успешного удаления
            } else {
                alert('Error deleting ' + itemType + ': ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

document.getElementById('direction_id').addEventListener('change', function() {
    var directionId = this.value;
    fetch('/get_seats_for_' + directionId)
        .then(response => response.json())
        .then(data => {
            var seatSelect = document.getElementById('seat_id');
            seatSelect.innerHTML = '';
            data.forEach(seat => {
                var option = document.createElement('option');
                option.value = seat.seat_id;
                option.textContent = `${seat.class_field} - ${seat.seat_place} - ${seat.carriage} - ${seat.train_id}`;
                seatSelect.appendChild(option);
            });
        });
});
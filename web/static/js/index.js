function updateItem(itemId, description, date) {
    fetch('/update-item', {
        method: 'PATCH',
        body: JSON.stringify({ itemId: itemId, description: description, date: date })
    }).then((_res) => {
        window.location.href = '/'
    })
}


function updateItemModal(itemId) {
    const newDescription = document.getElementById(`editItemInput${itemId}`).value;
    const newdate = document.getElementById(`datetimepicker${itemId}`).value;
    updateItem(itemId, newDescription, newdate);
}

function deleteItem(itemId) {
    fetch('/delete-item', {
        method: 'DELETE',
        body: JSON.stringify({ itemId: itemId })
    }).then((_res) => {
        window.location.href = '/'
    })
}

$(function () {
    $('#datetimepicker').datetimepicker({
        minDate: moment(),
        format: 'YYYY-MM-DD HH:mm',
    });
});

$(function () {
    $('.datetimepicker-input').datetimepicker({
        minDate: moment(),
        format: 'YYYY-MM-DD HH:mm',
    });
});